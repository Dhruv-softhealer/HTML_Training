# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models, api

class PublishedBook(models.Model):
    _name = 'sh.book.published'
    _description = 'Book Published'
    
    name = fields.Char(string='Book Name')
    author_name = fields.Many2one(comodel_name='res.partner',string="Author Name")
    # def get_now(self):
    #     return fields.Datetime.now()
    published_date = fields.Datetime(default=fields.Datetime.now())
    age = fields.Char(string="Age", compute='_count_age')

    
    @api.model_create_multi
    def create(self, vals_list):
        # self.age = fields.datetime.now()
        res = super(PublishedBook, self).create(vals_list)
        res.published_date = fields.Datetime.now()
        return res
    
    @api.depends('published_date')
    def _count_age(self):
        for res in self:
            if res.published_date:
                total_sec = (fields.Datetime.now() - res.published_date).seconds

                days = total_sec // 86400
                total_sec %= 86400
                hours = total_sec // 3600
                total_sec %= 3600
                minutes = total_sec // 60
                total_sec %= 60
                

                if days>0:
                    res.age = f"{days} days {hours} hours {minutes} minutes {total_sec} seconds"
                elif hours>0:
                    res.age = f"{hours} Hours {minutes} minutes {total_sec} seconds"
                elif minutes>0:
                    res.age = f"{minutes} minutes {total_sec} seconds"
                elif total_sec>=0:
                    res.age = f"{total_sec} seconds"
            else:
                res.age='0'