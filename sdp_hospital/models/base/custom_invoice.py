# -*- coding: utf-8 -*-
from contextlib import nullcontext

from odoo import api, fields, models, _, tools, Command
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
from odoo.tools.sql import SQL
from bisect import bisect_left
from collections import defaultdict
import re
from odoo.addons.sdp_hospital.models.patterns.observer import PaymentObserver


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
    journal_type = fields.Selection(selection=[
        ('invoice', 'Invoice'),
        ('payment', 'Payment'),
    ],default='invoice')
    paid = fields.Boolean()
    journal_lines = fields.Boolean(compute="_compute_journal_lines",store=True)

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
        self.sudo().write({'paid':True})
        self.add_payment_journals()
        # Notify observers after payment registration
        observer = PaymentObserver()
        observer.payment_registered(self)

    def add_payment_journals(self):
        journal = self.env['custom.journal'].sudo().create({
            'patient_id': self.patient_id.id,
            'journal_type':'payment',
            'state':'confirmed',
        })
        receivable = self.env['custom.account'].sudo().search([('account_type','=','asset_receivable')],limit=1)
        cash = self.env['custom.account'].sudo().search([('account_type','=','asset_cash')],limit=1)
        total = sum([line.total_price for line in self.product_line_ids])
        self.env['custom.journal.line'].sudo().create({
            'custom_journal_id':journal.id,
            'credit':total,
            'label':"Customer Payment",
            'account_id':receivable.id,
        })
        self.env['custom.journal.line'].sudo().create({
            'custom_journal_id':journal.id,
            'debit':total,
            'label':"Customer Payment",
            'account_id':cash.id,
        })


    @api.depends('product_line_ids.product_id')
    def _compute_journal_lines(self):
        for rec in self:
            rec.journal_lines = True
            for each in rec.product_line_ids:
                receivable = self.env['custom.account'].sudo().search([('account_type','=','asset_receivable')],limit=1)
                income = self.env['custom.account'].sudo().search([('account_type','=','income')],limit=1)

                self.env['custom.journal.line'].sudo().create({
                    'custom_journal_id':rec.id,
                    'debit':each.total_price,
                    'label':rec.name,
                    'account_id':receivable.id,
                })
                self.env['custom.journal.line'].sudo().create({
                    'custom_journal_id':rec.id,
                    'credit':each.total_price,
                    'label':each.product_id.name,
                    'account_id':income.id,
                })
        


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
    label = fields.Char()
