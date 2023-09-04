import urllib.parse
from odoo import fields, _,models,api
from datetime import datetime
from odoo.exceptions import ValidationError
from collections import defaultdict



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
    last_action = fields.Datetime(string='Last Action',default=fields.Datetime.now)
    quantity = fields.Integer(string='Quantity')
    child_id = fields.Many2one('res.partner',string='Child Tags', domain="['&',('parent_id','=', partner_id),('hide_in_contact', '=', False)]")
    email_from = fields.Char(
        'Email', tracking=40, index=True,
        compute='_compute_email_from', inverse='_inverse_email_from', readonly=False, store=True)
    function = fields.Char('Job Position', compute='_compute_function', readonly=False, store=True)
    phone = fields.Char(
        'Phone', tracking=50,
        compute='_compute_phone', inverse='_inverse_phone', readonly=False, store=True)
    mobile = fields.Char('Mobile', compute='_compute_mobile', readonly=False, store=True)
    ref_number = fields.Char(string='Reference number')
    item_ids = fields.One2many('item.item','lead_id', string='Item')



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


    def action_send_mail(self):
        template = self.env.ref('crm_lead.email_template_crm_lead')
        for rec in self:
            template.send_mail(rec.id , force_send=True)



    def action_share_whatsapp(self):
        invoice_data = self.read()[0]
        if not self.child_id.phone:
            raise ValidationError(_('Missing Phone Number in Customer Record'))
        pdf_content = self.env [ 'ir.actions.report' ].sudo( )._render_pdf( [ invoice_data [ 'id' ] ] ,
                                                                            'account.report_invoice' ).decode( 'utf-8' )
        msg = 'Hi %s ' % self.child_id.name
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.child_id.phone,msg)
        return {
            'type' : 'ir.actions.act_url',
            'target' : 'new',
            'url' : whatsapp_api_url
        }

    def generate_reports(self) :
        company = self.env.user.company_id
        selected_leads = self.env [ 'crm.lead' ].browse( self.env.context.get( 'active_ids' , [ ] ) )

        if not selected_leads :
            raise ValidationError( _( 'No leads selected' ) )

        # Group the selected leads by assigned contact email
        assigned_contacts = {}  # Dictionary to store data for each contact's leads
        for lead in selected_leads :
            contact_email = lead.child_id.email
            if contact_email :
                if contact_email not in assigned_contacts :
                    assigned_contacts [ contact_email ] = [ ]
                assigned_contacts [ contact_email ].append( lead )

        # Process each assigned contact and send an email or raise an error
        for contact_email , leads in assigned_contacts.items( ) :
            unique_emails = {lead.email_from for lead in leads}

            if len( unique_emails ) == 1 :
                formatted_result = "<table border='1' style='border-collapse: collapse; width: 50%; text-align: center';>"
                formatted_result += (
                    "<tr><th><font color='#220a99'>Item Name</font></th><th><font color='#220a99'>Reference Number</font></th>"
                    "<th><font color='#220a99'>Quantity</font></th><th><font color='#220a99'>Status</font></th></tr>")

                for lead in leads :
                    formatted_result += "<tr>"
                    formatted_result += "<td align='left' style='padding-left: 15px;'>{}</td>".format( lead.name )
                    formatted_result += "<td align='left' style='padding-left: 15px;'>{}</td>".format( lead.ref_number )
                    formatted_result += "<td align='right' style='padding-right: 15px;'>{}</td>".format( lead.quantity )
                    formatted_result += "<td align='left' style='padding-left: 15px;'>{}</td>".format(
                        lead.status_id.name )
                    formatted_result += "</tr>"
                formatted_result += "</table><br>"

                company_info = """<p>Thanks and Regards</p>                
                  <p><font color="red">{}</font><br>{}<br>{}</p>""".format( company.name , company.street ,
                                                                            company.phone )

                recipient_name = lead.child_id.name

                email_content = """               
                  <html>                
                  <body>                               
                  <p>Dear {},</p>                
                  <p>Greetings, Please find below list for your kind reference</p>                
                  {}                
                  {}                
                  </body>                
                  </html>            
                  """.format( recipient_name , formatted_result , company_info )

                # Send the email to this assigned contact
                mail_values = {
                    'subject' : 'Item Details' ,
                    'body_html' : email_content ,
                    'email_to' : contact_email ,
                }
                self.env [ 'mail.mail' ].create( mail_values ).send( )
            else :
                print( f"Error: Leads for contact {contact_email} have different email addresses." )

    # def action_share_whatsapp(self):
    #     selected_leads = self.env['crm.lead'].browse(self.env.context.get('active_ids', []))
    #
    #     if not selected_leads:
    #         raise ValidationError(_('No leads selected'))
    #
    #     base_whatsapp_url = 'https://api.whatsapp.com/send?text='
    #     phone_number_messages = defaultdict(list)
    #
    #     for lead in selected_leads:
    #         if not lead.child_id.phone:
    #             raise ValidationError(_('Missing Phone Number for lead %s') % lead.name)
    #
    #         msg = 'Hi, here is the CRM Lead Report:\n\n'
    #         msg += "Lead: {}\n".format(lead.name)
    #         msg += "Reference Number: {}\n".format(lead.ref_number)
    #         msg += "Email: {}\n".format(lead.email_from)
    #         msg += "Phone: {}\n".format(lead.phone)
    #         msg += "Quantity: {}\n".format(lead.quantity)
    #         msg += "Status: {}\n".format(lead.status_id.name)
    #         msg += "\n"
    #
    #         encoded_msg = urllib.parse.quote(msg)
    #         whatsapp_api_url = base_whatsapp_url + encoded_msg
    #         phone_number_messages[lead.child_id.phone].append(whatsapp_api_url)
    #
    #     for phone_number, messages in phone_number_messages.items():
    #         final_whatsapp_urls = ','.join(messages)
    #
    #         return {
    #             'type': 'ir.actions.act_url',
    #             'target': 'new',
    #             'url': final_whatsapp_urls,
    #         }



class Item(models.Model):
    _name = 'item.item'

    lead_id = fields.Many2one('crm.lead', string='Item Name')
    name = fields.Char(string='Item Name')
    quantity = fields.Integer(string='Quantity')
    ref_number = fields.Char(string='Reference number')
    status_id = fields.Many2one("status.status", string="Status")






