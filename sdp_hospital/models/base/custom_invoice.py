# -*- coding: utf-8 -*-
from contextlib import nullcontext

from odoo import api, fields, models, _, tools, Command
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
from odoo.tools.sql import SQL
from bisect import bisect_left
from collections import defaultdict
import re

class CustomJournal(models.Model):
    _name = "custom.journal"
    _inherit = ['mail.thread','mail.activity.mixin', 'image.mixin']
    _description = "Custom Journals"

   
    name = fields.Char(string="Account Name", required=True, index='trigram', tracking=True, translate=True)
    patient_id = fields.Many2one('medical.patient')
    line_ids = fields.One2many('custom.journal.line','custom_journal_id')
    product_line_ids = fields.One2many('medical.prescription','custom_journal_id')
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ("cancelled", "Cancelled")
    ])
    paid = fields.Boolean()

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name') or vals['name'] == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'custom.journal') or _('New')
        return super().create(vals_list)

    def action_confirm(self):
        self.state = 'confirmed'

    def action_reset_to_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_register_payment(self):
        pass


class CustomJournalLines(models.Model):
    _name = "custom.journal.line"
    _inherit = ['mail.thread','mail.activity.mixin', 'image.mixin']
    _description = "Custom Journal Line"

    custom_journal_id = fields.Many2one('custom.journal')
    account_id = fields.Many2one('custom.account')
    debit = fields.Monetary()
    credit = fields.Monetary()
    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.company)
    currency_id = fields.Many2one(related="company_id.currency_id",store=True)
    name = fields.Char(related="account_id.name",store=True)
