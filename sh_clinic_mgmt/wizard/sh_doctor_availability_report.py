# -*- coding: utf-8 -*-
# Part of Softhealer Technologies


from odoo import models, fields, api
from odoo.exceptions import UserError
from io import BytesIO
import xlsxwriter
import base64

class DoctorAvailabilityWizard(models.Model):
    _name = 'sh.doctor.availability.report'
    _description = 'Doctor Availability'
    
    # ==================================================================
    #                       Generate PDF Format
    # ==================================================================

    def action_print_report(self):
        report_action = self.env.ref('sh_clinic_mgmt.doctor_availability_action').report_action(self)
        report_action.update({
            'close_on_report_download': True,
        })
        return report_action
    
    # ==================================================================
    #                       Generate Excel Format
    # ==================================================================
    
    def action_excel_report(self):
        report_data = self.env['report.sh_clinic_mgmt.doctor_availability_template']._get_report_values(self.ids)
        
        results = report_data.get('records', [])

        if not results:
            raise UserError("No data found for the selected criteria.")

        output = BytesIO()
        
        # =========== >>>> create workbook <<<< ===========
        
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Doctor Availability Report')

        # =========== >>>> Define Formats <<<< ===========

        heading_format = workbook.add_format({'font_size': 11, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1, 'bg_color': "#B8B4B490", 'font_color': 'white'})
        bold_header = workbook.add_format({'font_size': 9, 'bold': True, 'align': 'center', 'valign': 'vcenter', 'border': 1,})
        normal_record = workbook.add_format({'font_size': 8, 'valign': 'vcenter', 'border': 1, 'align': 'left'})

        worksheet.merge_range('A1:E2', "Doctor Availability Report", heading_format)
        
        # =========== >>>> Set column widths <<<< ===========
        
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 25)
        worksheet.set_column('C:C', 25)
        worksheet.set_column('D:D', 35)
        worksheet.set_column('E:E', 15)
        
        # =========== >>>> Headers <<<< ===========

        headers = ["Doctor Name", "Department", "Available Days", "Shift Timing", "Status"]
        for col, header in enumerate(headers):
            worksheet.write(3, col, header, bold_header)

        # =========== >>>> Write Data <<<< ===========

        row = 4
        for record in results:
            worksheet.write(row, 0, record.get('doctor_name', ''), normal_record)
            worksheet.write(row, 1, record.get('department_name', ''), normal_record)
            worksheet.write(row, 2, record.get('available_days', ''), normal_record)
            worksheet.write(row, 3, record.get('shift_timing', ''), normal_record)
            worksheet.write(row, 4, record.get('status', ''), normal_record)
            row += 1

        workbook.close()
        output.seek(0)
        
        # =========== >>>> create Attachments <<<< ===========
        
        filename = 'Doctor_Availability_Report.xlsx'
        attachment_vals = {
            'name': filename,
            'datas': base64.b64encode(output.read()),
            'res_model': 'ir.ui.view',
            'type': 'binary',
        }
        attachment_id = self.env['ir.attachment'].create(attachment_vals)
        output.close()

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment_id.id}?download=true',
            'target': 'new',
        }


class DoctorAvailabilityReport(models.AbstractModel):
    _name = 'report.sh_clinic_mgmt.doctor_availability_template'
    _description = 'Doctor Availability Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print(f"\n\n\n\t--------------> 20 ")
        query = '''
            WITH unique_schedules AS (
                SELECT DISTINCT
                    he.id AS doctor_id,
                    he.name AS doctor_name,
                    hd.name->>'en_US' AS department_name,
                    rca.dayofweek,
                    rca.hour_from,
                    rca.hour_to,
                    CASE
                        WHEN EXISTS (
                            SELECT 1
                            FROM sh_slots s
                            WHERE s.doctor_id = he.id
                        )
                        THEN 'Active'
                        ELSE 'Not Active'
                    END AS status
                FROM
                    hr_employee he
                LEFT JOIN
                    hr_department hd ON he.department_id = hd.id
                JOIN
                    resource_resource rr ON he.resource_id = rr.id
                JOIN
                    resource_calendar rc ON rr.calendar_id = rc.id
                JOIN
                    resource_calendar_attendance rca ON rc.id = rca.calendar_id
                WHERE
                    he.job_id IN (
                        SELECT id
                        FROM hr_job
                        WHERE name->>'en_US' = 'Doctor'
                    )
                    AND rca.day_period != 'lunch'
            ),

            monday_schedules AS (
                SELECT
                    doctor_id,
                    doctor_name,
                    department_name,
                    STRING_AGG(
                        DISTINCT CASE dayofweek
                            WHEN '0' THEN 'Mon'
                            WHEN '1' THEN 'Tue'
                            WHEN '2' THEN 'Wed'
                            WHEN '3' THEN 'Thu'
                            WHEN '4' THEN 'Fri'
                            WHEN '5' THEN 'Sat'
                            WHEN '6' THEN 'Sun'
                        END,
                        ', '
                    ) AS available_days,
                    ARRAY_AGG(
                        CASE
                            WHEN dayofweek = '0' THEN
                                TO_CHAR(TO_TIMESTAMP(hour_from::text, 'HH24.MI'), 'HH12:MI AM')
                                || ' - ' ||
                                TO_CHAR(TO_TIMESTAMP(hour_to::text, 'HH24.MI'), 'HH12:MI AM')
                        END
                    ) AS monday_timings,
                    status
                FROM
                    unique_schedules
                GROUP BY
                    doctor_id,
                    doctor_name,
                    department_name,
                    status
            ),

            cleaned_schedules AS (
                SELECT
                    doctor_name,
                    department_name,
                    available_days,
                    ARRAY_REMOVE(monday_timings, NULL) AS cleaned_timings,
                    status
                FROM
                    monday_schedules
            )

            SELECT
                doctor_name,
                department_name,
                available_days,
                STRING_AGG(
                    cleaned_timings[i],
                    ', '
                ) AS shift_timing,
                status
            FROM
                cleaned_schedules,
                UNNEST(ARRAY[1, 2]) WITH ORDINALITY AS t(i, pos)
            WHERE
                i <= CARDINALITY(cleaned_timings)
            GROUP BY
                doctor_name,
                department_name,
                available_days,
                status
            ORDER BY
                doctor_name;
            '''
        
        self.env.cr.execute(query)
        results = self.env.cr.dictfetchall()
        print(f"\n\n\n\t--------------> 46 results",results)

        return {
            'doc_ids': docids,
            'doc_model': 'sh.doctor.availability.report',
            'records': results,
        }
