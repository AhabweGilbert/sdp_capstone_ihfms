from odoo import api, fields, models, _
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class Prescription(models.Model):
    
    _name = 'medical.prescription'
    _description = 'Medical Descriptions'    
    _inherit = ['mail.thread','mail.activity.mixin', 'image.mixin']

    name = fields.Char(readonly=True, index='trigram',default=lambda self: _('New'),copy=False)
    health_record_id = fields.Many2one('health.record')
    patient_id = fields.Many2one(related="health_record_id.patient_id",store=True)
    product_id = fields.Many2one('product.product')
    dosage = fields.Many2one('medical.dosage')
    quantity = fields.Float()
    unit_price = fields.Float()
    total_price = fields.Monetary(compute="_compute_total_price",store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.company)
    currency_id = fields.Many2one(related="company_id.currency_id",store=True)
    custom_journal_id = fields.Many2one('custom.journal')



    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'medical.prescription') or _('New')
        return super().create(vals_list)

    @api.depends('quantity','unit_price')
    def _compute_total_price(self):
        for rec in self:
            rec.total_price = rec.quantity * rec.unit_price

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            if rec.product_id:
                rec.unit_price = rec.product_id.list_price
  