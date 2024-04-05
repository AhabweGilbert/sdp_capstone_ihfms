from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import ValidationError,RedirectWarning, UserError
from datetime import datetime, timedelta

class PaymentObserver:
    def payment_registered(self, payment_data):
        # Method to be called when payment is registered
        # You can implement any action here
        
        email_template = payment_data.env.ref('sdp_hospital.mail_template_payment_registered')
        context = {}
        context.update({
                'invoice_number':payment_data.line_ids[0].move_id.name,
            })
        for i in range(0,5):
            print("observer")
            print(payment_data.line_ids[0].move_id.name)
        email_values = {
            'email_to': payment_data.line_ids[0].move_id.partner_id.email,
            'email_cc': False,
            'auto_delete': True,
            'recipient_ids': [],
            'partner_ids': [],
            'scheduled_date': False,
        }
        with payment_data.env.cr.savepoint():
            email_template.with_context(**context).send_mail(
                payment_data.line_ids[0].move_id.partner_id.id, force_send=True, raise_exception=True, email_values=email_values, email_layout_xmlid='mail.mail_notification_light'
            )


class AccountPaymentRegisterInherit(models.TransientModel):
    _inherit = 'account.payment.register'

    def action_create_payments(self):
        res = super(AccountPaymentRegisterInherit, self).action_create_payments()

        # Notify observers after payment registration
        observer = PaymentObserver()
        observer.payment_registered(self)
        return res