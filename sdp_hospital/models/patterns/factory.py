from odoo import api, fields, models

class Account:
    def __init__(self, env, account_type, **kwargs):
        self.env = env
        self.account_type = account_type
        self.details = kwargs

    def create_record(self):
        account_vals = {
            'name': self.details.get('name', ''),
            'account_type': self.account_type,
            'code': self.details.get('code', ''),
        }
        account = self.env['custom.account'].create(account_vals)
        return account


class AccountFactory:
    def __init__(self, env):
        self.env = env

    def create_account(self, account_type, **kwargs):
        account = Account(self.env, account_type, **kwargs)
        return account.create_record()


class ReceivableFactory(AccountFactory):
    def __init__(self, env):
        super().__init__(env)

    def create_account(self, **kwargs):
        return super().create_account('asset_receivable', **kwargs)


class PayableFactory(AccountFactory):
    def __init__(self, env):
        super().__init__(env)

    def create_account(self, **kwargs):
        return super().create_account('liability_payable', **kwargs)
