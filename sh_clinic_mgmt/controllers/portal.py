# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import http, _
from odoo.osv.expression import AND, OR
from odoo.http import request
from odoo.addons.portal.controllers import portal
from odoo.tools import date_utils, groupby as groupbyelem
from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from odoo.addons.account.controllers.download_docs import _get_headers, _build_zip_from_data
from odoo.exceptions import AccessError,MissingError
from odoo import fields
import requests
import logging
import json

_logger = logging.getLogger(__name__)

class AppointmentPortal(CustomerPortal):

    # Portal Home Values

    def _prepare_home_portal_values(self, counters):
            values = super()._prepare_home_portal_values(counters)
            if 'appointment_count' in counters:
                values['appointment_count'] = request.env['sh.appointment'].sudo().search_count([
                    ('sh_patient_id', '=', request.env.user.partner_id.id)
                ])
            return values

    def _search_bar_domain(self,search,search_in):
        search_domains = []
        if search_in in ('all', 'name'):
            search_domains.append([('name', 'ilike', search)])
        if search_in in ('all', 'doctor'):
            search_domains.append([('sh_doctor_id.name', 'ilike', search)])
        if search_in in ('all', 'sh_date'):
            search_domains.append([('sh_date', 'ilike', search)])
        if search_in in ('all', 'sh_state'):
            search_domains.append([('sh_state', 'ilike', search)])

        return OR(search_domains) if search_domains else []
    
    
    @http.route(['/my/appointments', '/my/appointments/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_appointments(self, page=1, sortby=True, filterby="all", groupby=None, search=None, search_in='name', **kw):
        Appointment = request.env['sh.appointment'].sudo()
        partner_id = request.env.user.partner_id.id

        domain = [('sh_patient_id', '=', partner_id)]
        
        appointments_count = Appointment.search_count(domain)
        
        # Search and Filter Logic
        
        searchbar_sortings = {
            'new': {'label': _('Appointment'), 'order': 'create_date desc'},
            'doctor': {'label': _('Doctor'), 'order': 'sh_doctor_id'},
            'stage': {'label': _('Stage'), 'order': 'sh_state'},
        }

        if sortby not in searchbar_sortings:
            sortby = 'doctor'

        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'new': {'label': _('New'), 'domain': [('sh_state','=','new')]},
            'in_progress': {'label': _('In-Progress'), 'domain': [('sh_state','=','in_progress')]},
            'completed_appointment': {'label': _('Completed Appointment'), 'domain': [('sh_state','=','completed_appointment')]},
            'cancelled_appointment': {'label': _('Cancelled Appointment'), 'domain': [('sh_state','=','cancelled_appointment')]},
        }

        searchbar_inputs = {
            'all': {'label': _('Search in All'), 'input': 'all'},
            'name': {'label': _('Search in Name'), 'input': 'name'},
            'doctor': {'label': _('Search in Doctor'), 'input': 'doctor'},
            'sh_date': {'label': _('Search in Date'), 'input': 'sh_date'},
            'sh_state': {'label': _('Search in Stage'), 'input': 'sh_state'}
        }


        if filterby:
            domain += searchbar_filters[filterby]["domain"]

        search_bar_domain = self._search_bar_domain(search,search_in)
       
        if search_bar_domain:
            domain = AND([domain,search_bar_domain])
        
        # Sorting & Pagination Logic
        
        order = searchbar_sortings[sortby]["order"]
        url = "/my/appointments"
        pager = portal.pager(
            url=url,
            total=appointments_count,
            page=page,
            step=20,
            url_args={'sortby': sortby, 'search_in': search_in, 'search': search, 'filterby': filterby, 'groupby': groupby},
        )
        appointments = Appointment.search(domain, limit=20, offset=pager['offset'], order=order)      


        # Grouping Logic

        def resolve_nested_attr(obj, attr_path):
            for attr in attr_path.split('.'):
                obj = getattr(obj, attr, False)
                if not obj:
                    return ''
            return obj

        grouped_appointments = []
        if groupby and groupby != 'none':
            appointments = appointments.sorted(key=lambda a: resolve_nested_attr(a, groupby))
            grouped_appointments = [
                (g, list(records))
                for g, records in groupbyelem(appointments, lambda a: resolve_nested_attr(a, groupby))
            ]
        else:
            grouped_appointments = [(False, appointments)]
        
        # Prepare the response for rendering
        
        request.session['my_pager'] = appointments.ids
        
        return request.render("sh_clinic_mgmt.portal_my_appointments", {
            'appointments': appointments,
            'pager': pager,
            'page_name': 'appointments',
            
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            
            'searchbar_filters': searchbar_filters,
            'filterby': filterby,
            
            'searchbar_inputs':searchbar_inputs,
            'search':search,
            'search_in':search_in,
            
            'grouped_appointments': grouped_appointments,
            'groupby': groupby,
            
            'default_url': url,
        })
        
    # Pagination at Form Side
      
    def get_records_pager(self, ids, current):
        if current.id in ids and (hasattr(current, 'website_url') or hasattr(current, 'access_url')):
            attr_name = 'access_url' if hasattr(current, 'access_url') else 'website_url'
            idx = ids.index(current.id)
            prev_record = idx != 0 and current.browse(ids[idx - 1])
            next_record = idx < len(ids) - 1 and current.browse(ids[idx + 1])

            if prev_record and prev_record[attr_name] and attr_name == "access_url":
                prev_url = '%s?access_token=%s' % (prev_record[attr_name], prev_record._portal_ensure_token())
            elif prev_record and prev_record[attr_name]:
                prev_url = prev_record[attr_name]
            else:
                prev_url = prev_record

            if next_record and next_record[attr_name] and attr_name == "access_url":
                next_url = '%s?access_token=%s' % (next_record[attr_name], next_record._portal_ensure_token())
            elif next_record and next_record[attr_name]:
                next_url = next_record[attr_name]
            else:
                next_url = next_record

            return {
                'prev_record': prev_url,
                'next_record': next_url,
            }
        return {}

    # Portal Record Detail View
    
    @http.route(["/my/appointments/<int:appointment_id>"], type="http", auth="public", website=True)
    def my_portal_document(self, appointment_id, access_token=None, report_type=None, download=False):
        try:
            appointment = self._document_check_access('sh.appointment', appointment_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        # Report
        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(
                model=appointment,
                report_type=report_type,
                report_ref='sh_clinic_mgmt.report_appointment_action',
                download=download
            )
        # Fetch record list of current user
        # appointments = request.env['sh.appointment'].sudo().search([
        #     ('sh_patient_id', '=', request.env.user.partner_id.id)
        # ])

        history = request.session.get('my_pager',[]) 


        record_pager = self.get_records_pager(history, appointment)

        return request.render("sh_clinic_mgmt.portal_appointment_detail", {
            "appointment": appointment,
            "page_name": "appointments",
            "prev_record": record_pager.get('prev_record'),
            "next_record": record_pager.get('next_record'),
        })

        
    # Book Appointment Page
    
    @http.route('/book/appointment', type='http', auth="user", website=True)
    def book_appointment(self, **kw):
        # print("KW >>>", kw)
        selected_date = kw.get('sh_date') or fields.Date.today().strftime('%Y-%m-%d')

        values = {
            'doctors': request.env['hr.employee'].sudo().search([('job_id.name', '=', 'Doctor')]),
            'slots': request.env['sh.slot.schedule'].sudo().search([('sh_date', '=', selected_date)]),
            'selected_date': selected_date,
            'csrf_token': request.csrf_token(),
        }
        return request.render('sh_clinic_mgmt.book_appointment_form', values)


    # Submit Appointment Page

    @http.route('/submit/appointment', type='http', auth="user", website=True, methods=["POST"],csrf=False)
    def submit_appointment(self, **post):
        patient = request.env.user.partner_id
        print("\n\n\n\n======",patient)
        doctor_id = post.get('sh_doctor_id')
        slot_id = post.get('portal_slot')
        print("\n\n\n\n======doctor_id",doctor_id)
        print("\n\n\n\n======slot_id",slot_id)
        

        if not doctor_id or not slot_id:
            return request.redirect('/book/appointment')

        rec_apt = request.env['sh.appointment'].sudo().create({
            'sh_patient_id': patient.id,
            'sh_doctor_id': int(doctor_id),
            'sh_date': post.get('sh_date'),
            'sh_slt_id': int(slot_id),
            'sh_visit_type':"new",
            'sh_phone': post.get('sh_phone'),
        })
        print("\n\n\n\n======rec_apt",rec_apt.name)


    @http.route('/portal/slotdata', type="http",auth="user",methods=['POST'],website=True,csrf=False)
    def sh_slot_data(self, **kw):
        dic = {}
        print("\n\n\n\n====>kw.get('sh_date')",(kw.get('sh_doctor_id')))
        if kw.get('sh_date') and kw.get('sh_doctor_id'):
            sub_categ_list = []
            sub_categ_ids = request.env['sh.slot.schedule'].sudo().search(
                [('sh_date', '=', (kw.get('sh_date'))),('sh_slot_id.doctor_id','=',int(kw.get('sh_doctor_id')))])
            print("\n\n\n\n====>sub_categ_ids",sub_categ_ids)
            
            for sub in sub_categ_ids:
                sub_categ_dic = {
                    'id': sub.id,
                    'name': sub.name,
                }
                sub_categ_list.append(sub_categ_dic)
            dic.update({
                'sub_categories': sub_categ_list
            })
        else:
            dic.update({
                'sub_categories': []
            })
        return json.dumps(dic)
    