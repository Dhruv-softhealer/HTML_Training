# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, api

class AppointmentSummaryReport(models.AbstractModel):
    _name = 'report.sh_clinic_mgmt.appointment_report_template'
    _description = 'Appointment Summary Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        data = data or {}
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        doctor_id = data.get('doctor_id')

        # Build query for appointment
        query_appointment = '''
            SELECT  
                sh_date::DATE AS date,
                COUNT(*) AS total,
                SUM(CASE WHEN sh_state = 'completed_appointment' THEN 1 ELSE 0 END) AS completed_appointment,
                SUM(CASE WHEN sh_state = 'cancelled_appointment' THEN 1 ELSE 0 END) AS cancelled_appointment,
                SUM(CASE WHEN sh_state = 'pending' THEN 1 ELSE 0 END) AS pending,

                (
                    SUM(CASE WHEN sh_state = 'completed_appointment' THEN 1 ELSE 0 END) +
                    SUM(CASE WHEN sh_state = 'cancelled_appointment' THEN 1 ELSE 0 END) +
                    SUM(CASE WHEN sh_state = 'pending' THEN 1 ELSE 0 END)
                ) AS total
            FROM 
                sh_appointment
            WHERE 
                sh_date BETWEEN %s AND %s
                {doctor_filter}
            GROUP BY 
                sh_date::DATE
            ORDER BY 
                sh_date::DATE;
        '''

        # Handle doctor filter
        doctor_filter = ''
        params = [from_date, to_date]
        if doctor_id:
            doctor_filter = 'AND sh_doctor_id = %s'
            params.append(doctor_id)
        query_appointment = query_appointment.format(doctor_filter=doctor_filter)

        # Execute SQL query_appointment
        self.env.cr.execute(query_appointment, params)
        results = self.env.cr.dictfetchall()

        # Sort and prepare result
        summary = sorted(results, key=lambda x: x['date'])
        doctor = self.env['hr.employee'].browse(doctor_id) if doctor_id else None

        return {
            'doc_ids': docids,
            'doc_model': 'sh.appointment.summary.report',
            'data': data,
            'summary': summary,
            'doctor': doctor,
        }
