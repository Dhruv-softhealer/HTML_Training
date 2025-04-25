# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

import datetime
from odoo import _, models, fields, api
from odoo.exceptions import ValidationError
from odoo.sql_db import timedelta

class Appointment(models.Model):
    _name = 'sh.appointment'
    _description = 'Appointment'
    # _order = 'sh_emergency_case'
    
    # Header Page
    
    name = fields.Char(string="Appointment Number", required=True, tracking=True, readonly=True, default=lambda self: _('New'))
    sh_patient_id = fields.Many2one('res.partner', string="Patient Name", required=True, tracking=True)
    sh_doctor_id = fields.Many2one('hr.employee', string="Doctor Name", required=True, tracking=True)
    sh_doctor_specialization = fields.Char(string="Doctor Specialization", related="sh_doctor_id.sh_specialization")
    sh_date = fields.Date(string="Date", required=True, tracking=True)
    sh_slot_id = fields.Many2one('sh.slots.schedule', string="Slot", required=True)
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
        ("todays_appointment", "Today's Appointment"),
        ('in_progress', 'In Progress'),
        ('pending_appointment', 'Pending Appointment'),
        ('completed_appointment', 'Completed Appointment'),
        ('cancelled_appointment', 'Cancelled Appointment'),
    ])
    
    
    # ================================= SEQUENCE ==================================
    
    # @api.model_create_multi
    # def create(self, vals_list):
    #     for vals in vals_list:
    #         if vals.get('sh_appointment_number', ("New")) == ("New"):
    #             seq_date = fields.Datetime.context_timestamp(
    #                 self, fields.Datetime.to_datetime(vals['create_date'])
    #             ) if 'create_date' in vals else None
    #             vals['sh_appointment_number'] = self.env['ir.sequence'].with_company(vals.get('company_id')).next_by_code(
    #                 'sh.appointment', sequence_date=seq_date) or _("New")

    #     return super().create(vals_list)
    
    
    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            booking_dt = fields.Datetime.from_string(val.get('sh_date'))
            current_dt = fields.Datetime.now()
    
            b_str = booking_dt.strftime("B%y%m%d-%H%M")
            c_str = current_dt.strftime("C%y%m%d-%H%M")
 
            seq = self.env['ir.sequence'].next_by_code('sh.appointment')
 
            val['name'] = f"APT-{b_str}-{c_str}-{seq}"
 
        return super(Appointment, self).create(vals)
    
    
    @api.constrains('sh_emergency_case')
    def _count_emg_case(self):
        count = self.search_count([('sh_emergency_case', '=', True)])
        if count>4:
            raise ValidationError("You can't generate Emergency Case more then 10 cases")
        
     
    @api.onchange('sh_emergency_case')
    def onchange_emergency_case(self):
        if self.sh_emergency_case:
            self.sh_doctor_notified = True
            self.sh_assigned_doctor = self.sh_doctor_id
            
     
        
    @api.onchange('sh_date')
    def onchage_state_and_charge(self):
        if self.sh_doctor_id and self.sh_patient_id:
            
            if self.sh_date < datetime.date.today():
                self.sh_date = False
                return {
                    'warning': {
                        'title': "Invalid Date",
                        'message': "Date cannot be set earlier than today."
                    }
                }
                
            case_days = self.env.company.sh_case_days
            
            if (self.sh_date - self.sh_last_visited).days > case_days:
                self.sh_visit_type = 'new'
                self.sh_expected_revenue = self.sh_doctor_id.sh_new_case_charges
                
            else:
                self.sh_visit_type = 'old'
                self.sh_expected_revenue = self.sh_doctor_id.sh_old_case_charges
                
                
    # def float_time_to_hours_minutes(self, float_time):
    #     hours = int(float_time)
    #     minutes = int(round((float_time - hours) * 60))
    #     return hours, minutes
 
    # def hours_minutes_to_float_time(self, hours, minutes):
    #     return hours + minutes / 60.0
 
    # def publish(self):
    #     self.sh_stage = 'published'
        # print(self.hours_minutes_to_float_time(3,15))
        # print(self.float_time_to_hours_minutes(9.50))
 
    def generate_slot(self):
        self.ensure_one()
        self.sh_slot_lines.unlink()
 
        slot_minutes = int(self.sh_slot_time)
        calendar_id = self.hr_employee_id.resource_calendar_id
 
        if not calendar_id:
            raise ValueError("No working hours calendar defined for this employee.")
 
        current_date = self.sh_start_date
        while current_date <= self.sh_end_date:
            weekday = str(current_date.weekday())
 
            all_lines = calendar_id.attendance_ids.filtered(lambda a: a.dayofweek == weekday)
            if not all_lines:
                current_date += timedelta(days=1)
                continue

            working_lines = all_lines.filtered(lambda a: a.day_period != 'lunch')
            break_lines = all_lines.filtered(lambda a: a.day_period == 'lunch')

            break_ranges = []
            for b in break_lines:
                start_b = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=b.hour_from)
                end_b = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=b.hour_to)
                break_ranges.append((start_b, end_b))
 
            for line in working_lines:
                start_dt = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=line.hour_from)
                end_dt = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=line.hour_to)
 
                current_slot_start = start_dt
                while current_slot_start + timedelta(minutes=slot_minutes) <= end_dt:
                    current_slot_end = current_slot_start + timedelta(minutes=slot_minutes)
 
                    overlaps_break = any(
                        (br_start < current_slot_end and current_slot_start < br_end)
                        for br_start, br_end in break_ranges
                    )
                    if not overlaps_break:
                        self.env['sh.slot.line'].create({
                            'sh_slot_id': self.id,
                            'sh_date': current_date,
                            'sh_start_time': current_slot_start.hour + current_slot_start.minute / 60.0,
                            'sh_end_time': current_slot_end.hour + current_slot_end.minute / 60.0,
                        })

                    current_slot_start = current_slot_end

            current_date += timedelta(days=1)