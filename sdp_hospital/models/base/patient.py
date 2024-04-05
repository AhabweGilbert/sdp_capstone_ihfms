from odoo import api, fields, models, _
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError



class Patient(models.Model):
    _name = 'medical.patient'
    _description = 'medical patient'    
    _inherits = {'res.partner': 'partner_id'}
    _inherit = ['mail.thread','mail.activity.mixin', 'image.mixin']

    partner_id = fields.Many2one('res.partner', required=True, ondelete='cascade', auto_join=True, index=True,
        string='Related Partner', help='Partner-related data of the Patient')

    name = fields.Char(related='partner_id.name', inherited=True, readonly=False, tracking = True)
    email = fields.Char(related='partner_id.email', inherited=True, readonly=False, tracking = True)
    country_id = fields.Many2one(related='partner_id.country_id',inherited=True, readonly=False, tracking = True)
    phone = fields.Char()
    address =  fields.Char()
    external_system = fields.Selection(selection=[
        ('system_a', 'External System A'),
        ('system_b', 'External System B'),
        ('system_c', 'External System C'),
    ])
    image_1920 = fields.Binary(related="partner_id.image_1920", inherited=True,readonly=False,tracking = True)    
    active = fields.Boolean(related='partner_id.active',inherited=True,readonly=False,tracking=True,default=True)

    date_of_birth = fields.Date(string="Date of Birth")
    sex = fields.Selection([('m', 'Male'),('f', 'Female')], string ="Sex")
    patient_history = fields.Text(string="Patient History")
    blood_type = fields.Selection([('A', 'A'),('B', 'B'),('AB', 'AB'),('O', 'O')], string ="Blood Type")
    rh = fields.Selection([('-+', '+'),('--', '-')], string ="Rh")
    marital_status = fields.Selection([('s','Single'),('m','Married'),('w','Widowed'),('d','Divorced'),('x','Seperated')],string='Marital Status')
    deceased = fields.Boolean(string='Deceased')
    date_of_death = fields.Date(string="Date of Death")
    cause_of_death = fields.Char(string='Cause of Death')
    current_insurance = fields.Char(string="Insurance")

    diagonised_diseases = fields.One2many('health.record','patient_id')
    diagonised_diseases_len = fields.Integer(compute="_compute_diagonised_diseases_len")

    def _compute_diagonised_diseases_len(self):
        for rec in self:
            rec.diagonised_diseases_len = len(rec.diagonised_diseases)

    def view_health_records(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("sdp_hospital.action_health_record")
        domain = [('id', 'in', self.diagonised_diseases.ids)]
        context= {'default_patient_id':self.id}
        views = [(self.env.ref('sdp_hospital.view_health_record_tree').id, 'tree'), (False, 'form')]
        return dict(action, domain=domain, context=context, views=views)

        

    
class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    company_id = fields.Many2one('res.company', string='Company', required=True,
            default=lambda self: self.env.company)

