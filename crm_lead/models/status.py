from odoo import fields,models


class Status(models.Model):
    _name = "status.status"

    name = fields.Char(string="Name")