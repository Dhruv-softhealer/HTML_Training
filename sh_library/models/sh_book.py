# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models, api
from odoo.exceptions import UserError


class Book(models.Model):
    _name = 'sh.book'
    _description = 'Book Details'
    
    
    b_line_ids = fields.One2many('sh.bookline', 'b_line_id', string="Book LineIDs")
    
    category_id = fields.Many2one(related='b_line_ids.c_line_id', store=True,string="CategoryID", readonly=False)
    # cat_id = fields.Many2one(related='b_line_ids.c_line_id', string="CategoryID", readonly=False)
    name = fields.Char("Title of Book")
    authorname = fields.Char("Name of Author")
    pub_date = fields.Date("Publication Date", copy=False)
    isbn = fields.Integer("ISBN Number")
    language = fields.Selection([('gujarati', 'Gujarati'), ('hindi', 'Hindi'), ('english', 'English')], string="Language")
    pages = fields.Integer("Number of Pages")
    price = fields.Integer("Price")
    description = fields.Text("Description")
    bk_ids = fields.Many2many("sh.member", relation="sh_library_member_book", string="Books")
    
    
    @api.model_create_multi
    def create(self,vals):
        rec = super(Book,self).create(vals)
        print("\n\n\n\n\n",self,vals)
        self.env['sh.bookline'].create({'b_line_id':rec.id,'c_line_id':rec.category_id.id})
        # for rec in vals:
    #         if rec['category_id'] == False:
    #             raise ValidationError("Category Cannot be empty")
    #         return super(Book,self).create(rec)
        
        # =========== Print price where the category_id is Fiction ==============
        
        # partners = self.env['sh.book'].search([('category_id', '=', 'Fiction')])
        # for partner in partners:
        #     print(partner.price)
        return rec
    
    # ================= Delete record where category_id is Fiction ============
    def unlink(self):
        # print('\n\n\n\n\n==============34343343===========',self)
        for val in self:
            if val.price > 500:
                raise UserError("You can not delete %s Record because of it's price is greater then 500."%val.name)
        rtn = super(Book, self).unlink()
        return rtn
    
    
    def write(self, vals):
        print("\n\n\n\n\n\n\n =================== ",vals)
        # vals['isbn'] = 123
        res = super(Book, self).write(vals)
        print("\n\n\n\n\n\n\n =================== ",res)
        return res
    
    def copy(self, default=None):
        default = dict(default or {}, name=self.name + ' (Copied)')
        return super().copy(default)
    
    # def unlink(self):
    #     if len(self.bk_ids) > 1:
    #         return False 
    #     return super(Book,self).unlink()

    @api.onchange('name')
    def _set_category(self):
        if (isinstance(self.name,str)):
            if self.name.__contains__("Fiction"):
                self.category_id = self.env['sh.category'].search([('name','=','Fiction')])
            
            if self.name.__contains__('Science'):
                self.category_id = self.env['sh.category'].search([('name','=','Science')])
                


    
class Bookline(models.Model):
    _name = 'sh.bookline'
    _description = 'Book Line'
    
    b_line_id = fields.Many2one("sh.book", string="Books")
    c_line_id = fields.Many2one("sh.category", string="Category Line")
    
    
    @api.model
    def create(self,vals_list):
        vals_list = [vals_list]
        for rec in vals_list:
            record = self.env['sh.bookline'].search([('b_line_id','=',rec['b_line_id'])])
            if record:
                record.write({'c_line_id':rec['c_line_id']})
                return record
            else:
                return super(Bookline,self).create(vals_list)
            
    