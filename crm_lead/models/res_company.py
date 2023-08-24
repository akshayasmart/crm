from odoo import models,fields


class ResCompany(models.Model):
    _inherit = 'res.partner'

    hide_in_contact = fields.Boolean(string="Hide in Contacts")


