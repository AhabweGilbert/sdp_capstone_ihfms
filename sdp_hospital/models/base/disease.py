from odoo import api, fields, models, _
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class Disease(models.Model):
    
    _name = 'disease'
    _description = 'Disease'    
    _inherit = ['mail.thread','mail.activity.mixin', 'image.mixin']

    name = fields.Char()
    description = fields.Text()

class MedicalDosage(models.Model):
    
    _name = 'medical.dosage'
    _description = 'Dosage'    
    _inherit = ['mail.thread','mail.activity.mixin', 'image.mixin']

    name = fields.Char()
    description = fields.Text()