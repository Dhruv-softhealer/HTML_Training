# -*- coding: utf-8 -*-
# Part of Softhealer Technology.

from odoo import fields, models

class Animal(models.Model):
    _name = 'animal'
    
    
    height = fields.Float(string='Height')
    
    
class Dog(models.Model):
    _name = 'dog'
    _inherit = 'animal'
    
    sound = fields.Char(string='Sound')
    food = fields.Char(string='Food')
    
    
class Cat(models.Model):
    _name = 'cat'
    _inherit = 'animal'
    
    sounds = fields.Char(string='Sound')
    sleeping_time = fields.Char(string='Sleeping Time')
    
    
class Animal_more(models.Model):
    _inherit = 'animal'
    
    weight = fields.Float(string="Weight")

    
class Animal_extra(models.Model):
    _name = 'animal'
    _inherit = 'animal'
    
    color = fields.Float(string='Color')