# -*- coding: utf-8 -*-
# Part of Softhealer Technologies

from odoo import fields,models

class Parent(models.Model):
    _name = "sh.parent"

    parent_definition = fields.PropertiesDefinition("Definition")

class Child(models.Model):
    _name = "sh.child"

    parent_id = fields.Many2one("sh.parent")
    properties = fields.Properties(definition="parent_id.parent_definition")