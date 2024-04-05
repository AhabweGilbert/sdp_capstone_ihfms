from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from odoo.addons.sdp_hospital.models.patterns.factory import ReceivableFactory, PayableFactory

ACCOUNT_TYPES = {
    'asset_receivable': ReceivableFactory,
    'liability_payable': PayableFactory
}
class CreateAccountWizard(models.TransientModel):
    _name = 'create.account.wizard'
    _description = 'Create Account Wizard'

    code = fields.Char()
    name = fields.Char()
    account_type = fields.Selection(selection=[
        ('asset_receivable', 'Accounts Receivable'),
        ('liability_payable', 'Accounts Payable'),
        ("income", "Income"),
        ("asset_current", "Current Assets"),
        ("expense", "Expenses"),
    ], string="Account Type",required=True)

  
    def create_account(self):
        account_factory_class = ACCOUNT_TYPES.get(self.account_type)
        if account_factory_class:
            account_factory = account_factory_class(self.env)
            account = account_factory.create_account(name=self.name,code=self.code, initial_balance=0)
            return account
        else:
            raise UserError("Invalid account type: {}".format(self.account_type))

        return {
            'type': 'ir.actions.act_window_close',
        }


