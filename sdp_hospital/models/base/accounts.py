# -*- coding: utf-8 -*-
from contextlib import nullcontext

from odoo import api, fields, models, _, tools, Command
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
from odoo.tools.sql import SQL
from bisect import bisect_left
from collections import defaultdict
import re

class CustomAccount(models.Model):
    _name = "custom.account"
    _inherit = ['mail.thread','mail.activity.mixin', 'image.mixin']
    _description = "Custom Account"

   
    name = fields.Char(string="Account Name", required=True, index='trigram', tracking=True, translate=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.company)
    currency_id = fields.Many2one(related="company_id.currency_id",store=True)
    code = fields.Char(size=64, required=True, tracking=True, index=True, unaccent=False)
    account_type = fields.Selection(
        selection=[
            ("asset_receivable", "Receivable"),
            ("liability_payable", "Payable"),
            ("income", "Income"),
            ("asset_current", "Current Assets"),
            ("expense", "Expenses"), 
        ],
        string="Type", tracking=True,
        required=True,)
   
  