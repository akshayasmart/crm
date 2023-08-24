from odoo import models,fields


class Regarding(models.Model):
    _name = 'regarding.regarding'

    name = fields.Char(string='Regarding')