from odoo import api, fields, models
from abc import ABC, abstractmethod

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


class AccountCreatorFactory(ABC):
    def __init__(self, env):
        self.env = env

    @abstractmethod
    def create_account(self, account_type, **kwargs):
        pass



class ReceivableFactory(AccountCreatorFactory):
    def __init__(self, env):
        super().__init__(env)

    def create_account(self, **kwargs):
        account = Account(self.env, 'asset_receivable', **kwargs)
        return account.create_record()

class IncomeFactory(AccountCreatorFactory):
    def __init__(self, env):
        super().__init__(env)

    def create_account(self, **kwargs):
        account = Account(self.env, 'income', **kwargs)
        return account.create_record()

class AssetFactory(AccountCreatorFactory):
    def __init__(self, env):
        super().__init__(env)

    def create_account(self, **kwargs):
        account = Account(self.env, 'asset_current', **kwargs)
        return account.create_record()

class ExpenseFactory(AccountCreatorFactory):
    def __init__(self, env):
        super().__init__(env)

    def create_account(self, **kwargs):
        account = Account(self.env, 'expense', **kwargs)
        return account.create_record()

class AssetCashFactory(AccountCreatorFactory):
    def __init__(self, env):
        super().__init__(env)

    def create_account(self, **kwargs):
        account = Account(self.env, 'asset_cash', **kwargs)
        return account.create_record()

class PayableFactory(AccountCreatorFactory):
    def __init__(self, env):
        super().__init__(env)

    def create_account(self, **kwargs):
        account = Account(self.env, 'liability_payable', **kwargs)
        return account.create_record()


class AccountProductFactory(ABC):
    def __init__(self, env):
        self.env = env

    @abstractmethod
    def add_transaction(self, invoice_journal):
        pass

class ReceivableConcreteProduct(AccountProductFactory):
    def __init__(self, env):
        super().__init__(env)

    def add_transaction(self, invoice_journal):
        journal = self.env['custom.journal'].sudo().create({
            'patient_id': invoice_journal.patient_id.id,
            'journal_type':'payment',
            'state':'confirmed',
        })
        receivable = self.env['custom.account'].sudo().search([('account_type','=','asset_receivable')],limit=1)
        cash = self.env['custom.account'].sudo().search([('account_type','=','asset_cash')],limit=1)
        total = sum([line.total_price for line in invoice_journal.product_line_ids])
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