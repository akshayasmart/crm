from odoo import fields,models


class Category(models.Model):
    _name = "category.category"

    name = fields.Char(string="Name")



