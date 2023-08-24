from odoo import fields, models,api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    state = fields.Selection([('work_open', 'Work Open'),
                              ('work_closed', 'Work Closed')], string='State', default='work_open')
    partner_id = fields.Many2one(
        'res.partner', string='Customer',domain="['&',('hide_in_contact', '=', False),('parent_id','=', False)]")

    regarding_id = fields.Many2one('regarding.regarding', string='Regarding')

    street = fields.Char('Street', compute='_compute_partner_address_values', readonly=True, store=True)
    street2 = fields.Char('Street2', compute='_compute_partner_address_values', readonly=True, store=True)
    zip = fields.Char('Zip', change_default=True, compute='_compute_partner_address_values', readonly=True, store=True)
    city = fields.Char('City', compute='_compute_partner_address_values', readonly=True, store=True)
    state_id = fields.Many2one(
        "res.country.state", string='State',
        compute='_compute_partner_address_values', readonly=True, store=True,
        domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one(
        'res.country', string='Country',
        compute='_compute_partner_address_values', readonly=True, store=True)
    website = fields.Char('Website', index=True, help="Website of the contact", compute="_compute_website",
                          readonly=True, store=True)
    lang_id = fields.Many2one(
        'res.lang', string='Language',
        compute='_compute_lang_id', readonly=True, store=True)
    status_id = fields.Many2one("status.status", string="Status")
    category_id = fields.Many2one("category.category", string="Category")
    last_action = fields.Datetime(string='Last Action')
    quantity = fields.Integer(string='Quantity')
    child_id = fields.Many2one('res.partner',string='Child Tags', domain="[('parent_id','=', partner_id)]" )
    email_from = fields.Char(
        'Email', tracking=40, index=True,
        compute='_compute_email_from', inverse='_inverse_email_from', readonly=False, store=True)
    function = fields.Char('Job Position', compute='_compute_function', readonly=False, store=True)
    phone = fields.Char(
        'Phone', tracking=50,
        compute='_compute_phone', inverse='_inverse_phone', readonly=False, store=True)
    mobile = fields.Char('Mobile', compute='_compute_mobile', readonly=False, store=True)
    ref_number = fields.Char(string='Reference number')


    @api.depends('child_id.email')
    def _compute_email_from(self):
        for lead in self:
            if lead.child_id.email :
                lead.email_from = lead.child_id.email

    @api.depends('child_id')
    def _compute_function(self):
        """ compute the new values when partner_id has changed """
        for lead in self:
            if not lead.function or lead.child_id.function:
                lead.function = lead.child_id.function

    @api.depends('child_id.phone')
    def _compute_phone(self):
        for lead in self:
            if lead.child_id.phone:
                lead.phone = lead.child_id.phone

    @api.depends('child_id')
    def _compute_mobile(self):
        """ compute the new values when partner_id has changed """
        for lead in self:
            if not lead.mobile or lead.child_id.mobile:
                lead.mobile = lead.child_id.mobile
