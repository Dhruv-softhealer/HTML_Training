# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from datetime import datetime, timedelta
from odoo import Command, _, models, fields, api
from odoo.exceptions import ValidationError
from odoo.sql_db import timedelta
from odoo.tools.date_utils import date

class Appointment(models.Model):
    _name = 'sh.appointment'
    _description = 'Appointment'
    # _order = 'sh_emergency_case'
    
    # Header Page
    
    name = fields.Char(string="Appointment Number", required=True, tracking=True, readonly=True, default=lambda self: _('New'))
    sh_patient_id = fields.Many2one('res.partner', string="Patient Name", required=True, tracking=True)
    sh_doctor_id = fields.Many2one('hr.employee', string="Doctor Name", required=True, tracking=True)
    sh_doctor_specialization = fields.Char(string="Doctor Specialization", related="sh_doctor_id.sh_specialization")
    sh_date = fields.Datetime(string="Date", required=True, tracking=True)
    sh_slot_id = fields.Many2one('sh.slots',required=True,string='Slot')
    sh_status = fields.Selection([
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string="Status", required=True, tracking=True)
    sh_expected_revenue = fields.Float(string="Case Charges", required=True, tracking=True)
    sh_emergency_case = fields.Boolean(string="Emergency Case", tracking=True)
    
    
    # Patient Details 

    sh_email = fields.Char(string="Email", related="sh_patient_id.email", required=True)
    sh_phone = fields.Char(string="Phone", related="sh_patient_id.phone", required=True, readonly=False)
    sh_blood_group = fields.Selection(string="Blood Group", related="sh_patient_id.sh_blood_group")
    sh_birth_date = fields.Date(string="Birth Date", related="sh_patient_id.sh_birth_date", required=True)
    sh_age = fields.Char(string="Age", related="sh_patient_id.sh_age", required=True)
    sh_visit_type = fields.Selection([
        ('new', 'New'),
        ('old', 'Old')
    ], string="Visit Type", required=True)
    sh_last_visited = fields.Date(string="Last Visited", related="sh_patient_id.sh_last_visit_date", required=True)
    
    
    # Disease Details
    
    sh_disease_line = fields.One2many('sh.disease.detail', 'sh_disease_o2m_id')
    
    
    # Prescription & Medication 
    
    sh_prescription_line = fields.One2many('sh.prescription.madication', 'sh_prescription_o2m_id')
    
    # Personal medical info
    
    sh_lifestyle_factors_ids = fields.Many2many('sh.life.style.fector', related="sh_patient_id.sh_life_style_fector_ids", string="LifeStyle Fector")
    sh_mental_health_issues_ids = fields.Many2many('sh.mental.health.problem', related="sh_patient_id.sh_mental_health_problem_ids", string="Mental Health Issues")
    sh_chronic_conditions_ids = fields.Many2many('sh.chronic.condition', related="sh_patient_id.sh_cronic_condition_ids", string="Chronic Condition")
    sh_dietary_preferences = fields.Selection(string="Dietary Preferences", related="sh_patient_id.sh_dietary_preferences")
    sh_allergy_ids = fields.Many2many('sh.allergies', string="Allergies", related="sh_patient_id.sh_allergy_ids")
    
    # Emergency Handling info
    
    sh_priority_level = fields.Selection([
        ('normal', 'Normal'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], string="Priority Level", tracking=True)
    sh_doctor_notified = fields.Boolean(string="Doctor Notified?")
    sh_assigned_doctor = fields.Many2one('hr.employee', string="Assigned Doctor", tracking=True)
    sh_immediate_check_in = fields.Boolean(string="Immediate Check-in?", tracking=True)
    sh_emergency_slot_bypass = fields.Boolean(string="Emergency Slot Bypass", tracking=True)
    sh_walk_in_case = fields.Boolean(string="Walk In Case?", tracking=True)
    sh_checked_in = fields.Boolean(string="Checked In?")
    
    sh_state = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed_appointment', 'Completed Appointment'),
        ('cancelled_appointment', 'Cancelled Appointment'),
    ], 
    default='new'
    )

    sh_is_locked = fields.Boolean()
    
    
    # ===================================== Onchange Emergency Boolean ===========================================
    
    @api.onchange('sh_emergency_case')
    def _onchange_emergency_case(self):
        if self.sh_emergency_case:
            return{
                'name': 'Switch to Emergency',
                'type': 'ir.actions.act_window',
                'res_model': 'sh.emergency.case.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_message': 'Are you sure you want to switch to emergency case?'
                }
            }
    
    
    # ===================================== Stages ===========================================
    
 
    def check_in(self):
        self.sh_state = 'in_progress'
        self.sh_checked_in = True
        
    def move_to_done(self):
        self.sh_state = 'completed_appointment'
        self.sh_patient_id.sh_last_visit_date = date.today()
        self.sh_is_locked = True
        return {
        'type': 'ir.actions.client',
        'tag': 'reload',
        }
        
    def unlock_record(self):
        self.sh_state = 'unlock'
    
    def calcel_record(self):
        local_booking_dt = fields.Datetime.context_timestamp(self, self.sh_date)
        now_dt = fields.Datetime.context_timestamp(self, datetime.now())
        rec = self.env['sh.slots'].browse(self.sh_slot_id.id)
        # print("\n\n\n\n", rec)

        if rec.sh_cancel_time:
            cancel_time = rec.sh_cancel_time
            diff = (local_booking_dt - now_dt).total_seconds() / 3600.0
            print("\n\n\n\n", diff)
            if diff < cancel_time:
                raise ValidationError(f"You can't cancel before {cancel_time} hours from your booking time.")
            else:
                slot_line = self.env['sh.slot.schedule'].search([('sh_slot_id', '=', self.sh_slot_id.id),('sh_appointment_line', 'in', self.id)],limit=1)
                print("\n\n\n\n", slot_line)
                slot_line.write({
                    'sh_appointment_line': [Command.unlink(self.id)]
                })
                self.sh_state = 'cancelled_appointment'
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Success',
                        'message': 'Appointment cancelled successfully.',
                        'type': 'success',  
                        'sticky': False,
                    }
                }
    
        
    
    # ======================================= Emergence Case Count ==========================================
    
    @api.constrains('sh_emergency_case')
    def _count_emg_case(self):
        count = self.search_count([('sh_emergency_case', '=', True)])
        if count>4:
            raise ValidationError(f"You can't generate Emergency Case more then {count} cases")
        
     
    @api.onchange('sh_emergency_case')
    def onchange_emergency_case(self):
        if self.sh_emergency_case:
            self.sh_doctor_notified = True
            self.sh_assigned_doctor = self.sh_doctor_id
            
     
    # ======================================= Date Validation & Apply Charges ==========================================
        
    @api.onchange('sh_date')
    def onchage_state_and_charge(self):
        if self.sh_doctor_id and self.sh_patient_id:
            
            if self.sh_date <= fields.datetime.today():
                self.sh_date = False
                return {
                    'warning': {
                        'title': "Invalid Date",
                        'message': "Date cannot be set earlier than today."
                    }
                }
                
            case_days = self.env.company.sh_case_days
            
            if (self.sh_date.date() - self.sh_last_visited).days > case_days:
                self.sh_visit_type = 'new'
                self.sh_expected_revenue = self.sh_doctor_id.sh_new_case_charges
                
            else:
                self.sh_visit_type = 'old'
                self.sh_expected_revenue = self.sh_doctor_id.sh_old_case_charges

 
# ======================================== Time Validation =========================================

    def assign_slot_line(self):
        if self.sh_slot_id and self.sh_date:
            slot_time = fields.Datetime.context_timestamp(self, self.sh_date).time()
            slot_time_float = slot_time.hour + slot_time.minute / 60.0
            # print("\n\n\n\n", slot_time_float)
            
            slot_line = self.sh_slot_id.sh_schedule_line.filtered(
                lambda a: (a.sh_start_time <= slot_time_float and a.sh_end_time > slot_time_float) and a.sh_date == self.sh_date.date()
            )
            if not slot_line:
                raise ValidationError("Please change the time, Slot Time is not available.")
            if not self.sh_emergency_slot_bypass:
                if len(slot_line.sh_appointment_line) >= self.sh_slot_id.sh_allowed_patients:
                    raise ValidationError(f"Only {self.sh_slot_id.sh_allowed_patients} Patients allowed in {self.sh_slot_id.name}")
            
                slot_line.write({
                    'sh_appointment_line': [Command.link(self.id)]
                })
            else:
                slot_line.write({
                    'sh_appointment_line': [Command.link(self.id)]
                })
                

# ================================== Sequence =======================================
   
    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if val['sh_date']:
                booking_dt = fields.Datetime.from_string(val['sh_date'])
                                
                local_booking_dt = fields.Datetime.context_timestamp(self, booking_dt)
                booking_str = local_booking_dt.strftime('%y%m%d-%H%M')
 
                now_dt = fields.Datetime.context_timestamp(self, datetime.now())
                current_str = now_dt.strftime('%y%m%d-%H%M')
                
                #============================ pre-booking validation =================================
                
                if val['sh_slot_id'] and not val['sh_emergency_slot_bypass']:
                    rec = self.env['sh.slots'].browse(val['sh_slot_id'])
                    if rec.sh_pre_booking:
                        pre_booking_hour = rec.sh_pre_booking
                        diff = (local_booking_dt - now_dt).total_seconds() / 3600.0
            
                        if diff < pre_booking_hour:
                            raise ValidationError(f"A minimum advance booking of {pre_booking_hour} hours is required.")
 
                seq = self.env['ir.sequence'].next_by_code('sh.appointment') or '000'
                val['name'] = f'APT-B{booking_str}-C{current_str}-{seq}'
           
        record = super().create(vals)
        record.assign_slot_line()
        return record
 
    def write(self, vals):
        res = super(Appointment, self).write(vals)
 
        if 'sh_date' in vals or 'sh_slot_id' in vals or 'sh_emergency_slot_bypass' in vals:
            if vals.get('sh_date'):
                booking_dt = fields.Datetime.from_string(vals['sh_date'])
                local_booking_dt = fields.Datetime.context_timestamp(self, booking_dt)
 
            now_dt = fields.Datetime.context_timestamp(self, datetime.now())
            
            
            #============================ pre-booking validation =================================
            
            if vals.get('sh_slot_id') and not vals.get('sh_emergency_slot_bypass'):
                rec = self.env['sh.slots'].browse(vals['sh_slot_id'])
                if rec.sh_pre_booking:
                    pre_booking_hour = rec.sh_pre_booking
                    diff = (local_booking_dt - now_dt).total_seconds() / 3600.0
                   
                    if diff < pre_booking_hour:
                        raise ValidationError(f"A minimum advance booking of {pre_booking_hour} hours is required.")
 
            slot_line = self.env['sh.slot.schedule'].search([('sh_slot_id', '=', self.sh_slot_id.id),('sh_appointment_line', 'in', self.id)],limit=1)
                        
            slot_line.write({
                'sh_appointment_line': [Command.unlink(self.id)]  
            })
                        
            self.assign_slot_line()
        return res