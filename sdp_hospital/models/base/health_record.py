from odoo import api, fields, models, _, Command

from datetime import date,datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class HealthRecord(models.Model):
    
    _name = 'health.record'
    _description = 'Health Record'    
    _inherit = ['mail.thread','mail.activity.mixin', 'image.mixin']

    name = fields.Char(readonly=True, index='trigram',default=lambda self: _('New'),copy=False)
    patient_id = fields.Many2one('medical.patient')
    disease = fields.Many2one('disease')
    medical_history = fields.Text()
    procedures = fields.Text()
    prescription_ids = fields.One2many('medical.prescription','health_record_id')
    bill_created = fields.Boolean()
    custom_journal_id = fields.Many2one('custom.journal')

    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'health.record') or _('New')
        return super().create(vals_list)

    def create_bill(self):
        custom_invoice = self.env['custom.journal'].create({
            'patient_id': self.patient_id.id,
        })
        for each in self.prescription_ids:
            each.custom_journal_id = custom_invoice.id
        custom_invoice.action_confirm()
        self.bill_created = True
        self.custom_journal_id = custom_invoice.id
        return {
                'name':'Custom Invoice',
                'res_model':'custom.journal',
                'type':'ir.actions.act_window',
                'view_mode':'form',
                'view_id':self.env.ref('sdp_hospital.view_custom_invoice_form').id,
                'res_id': custom_invoice.id,
            }
        
        # return 

    def view_invoice(self):
        return {
                'name':'Custom Invoice',
                'res_model':'custom.journal',
                'type':'ir.actions.act_window',
                'view_mode':'form',
                'view_id':self.env.ref('sdp_hospital.view_custom_invoice_form').id,
                'res_id': self.custom_journal_id.id,
            }
   