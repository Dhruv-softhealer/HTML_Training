# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import http, _
from odoo.osv.expression import AND, OR
from odoo.http import request
from odoo.addons.portal.controllers import portal
from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from odoo.exceptions import AccessError,MissingError

class AppointmentPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        values['appointment_count'] = request.env['sh.appointment'].sudo().search_count([
            ('sh_patient_id', '=', request.env.user.partner_id.id)
        ])
        return values

    def _ticket_get_searchbar_groupby(self):
        return {
            'none': {'label': _('None'), 'sequence': 10},
            'name': {'label': _('Appointments'), 'sequence': 20},
            'doctor': {'label': _(''), 'sequence': 30},
            'sh_date': {'label': _('Stage'), 'sequence': 40},
            'stage': {'label': _('Status'), 'sequence': 50},
        }

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

        print('\n\n\n\n')
        print(f'---old-search_domains----> {search_domains}')
        print('\n\n\n\n')
        return OR(search_domains) if search_domains else []

    @http.route(['/my/appointments'], type='http', auth="user", website=True)
    def portal_my_appointments(self, page=1, sortby=True, filterby="all", groupby=None, search=None, search_in='name', **kw):
        Appointment = request.env['sh.appointment'].sudo()
        partner_id = request.env.user.partner_id.id

        domain = [('sh_patient_id', '=', partner_id)]
        
        appointments_count = Appointment.search_count(domain)
        
        pager = portal.pager(
            url="/my/appointments",
            total=appointments_count,
            page=page,
            step=10,
            url_args={},
        )
        # print("\n\n\n\nPager for appointments---->:", pager)

        appointments = Appointment.search(domain, limit=10, offset=pager['offset'], order='sh_date')
        # print("\n\n\n\nAppointments---->:", appointments)
        
        searchbar_groupings = {
            None: {'label': _('None')},
            'name': {'label': _('Appointment'), 'groupby': 'name'},
            'doctor': {'label': _('Doctor'), 'groupby': 'sh_doctor_id'},
            'sh_date': {'label': _('Date'), 'groupby': 'sh_date'},
            'stage': {'label': _('Stage'), 'groupby': 'sh_state'},
        }
        
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

        order = searchbar_sortings[sortby]["order"]

        if filterby:
            domain += searchbar_filters[filterby]["domain"]

        search_bar_domain = self._search_bar_domain(search,search_in)
       
        print('\n\n\n\n')
        print(f'----search_bar_domain----> {search_bar_domain}')
        print('\n\n\n\n')

        if search_bar_domain:
            domain = AND([domain,search_bar_domain])

        print('\n\n\n\n')
        print(f'----domain----> {domain}')
        print('\n\n\n\n')
        url = "/my/transfer"
        pager_values = portal.pager(
            url=url,
            total=Appointment.search_count(domain=domain),
            page=page,
            step=50,
            url_args={},
        )
        appointments = Appointment.search(domain, order=order , limit=50,offset=pager_values["offset"])
        
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
            
            'searchbar_groupings': searchbar_groupings,
            'groupby': groupby,
            
            'default_url': url,
        })
        
    def _get_prev_next_ids(self, current_id):
        ids = request.env['sh.appointment'].search([], order='id').ids
        current_index = ids.index(current_id)
        prev_id = ids[current_index - 1] if current_index > 0 else None
        next_id = ids[current_index + 1] if current_index < len(ids) - 1 else None
        return prev_id, next_id
        
    @http.route(['/my/appointments/<int:appointment_id>'], type='http', auth="user", website=True)
    def portal_appointment_detail(self, appointment_id, **kw):
        appointment = request.env['sh.appointment'].sudo().browse(appointment_id).exists()
        prev_id, next_id = self._get_prev_next_ids(appointment_id)
        if not appointment or appointment.sh_patient_id.id != request.env.user.partner_id.id:
            return request.redirect('/my/appointments')
    
        return request.render("sh_clinic_mgmt.portal_appointment_detail", {
            'appointment': appointment,
            'page_name': 'appointments',
            'document': appointment,
            'prev_id': prev_id,
            'next_id': next_id,
        })