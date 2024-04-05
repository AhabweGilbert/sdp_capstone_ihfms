import xml.etree.ElementTree as ET
from odoo import api, fields, models, _

class ExternalDataAdapter:
    def __init__(self, external_xml):
        self.external_xml = external_xml
    
    def convert_to_dictionary_format(self):
        dictionary_records = []
        root = ET.fromstring(self.external_xml)
        for patient in root.findall('patient'):
            name = patient.find('patient_name').text
            age = int(patient.find('patient_age').text)
            diagnosis = patient.find('patient_diagnosis').text
            email =  patient.find('email').text
            phone = patient.find('phone').text
            
            odoo_record = {
                'name': name,
                # 'age': age,
                'patient_history': diagnosis,
                'email':email,
                'phone':phone,
            }
            dictionary_records.append(odoo_record)
        return dictionary_records


class PatientFetchWizard(models.TransientModel):
    _name = 'patient.wizard'
    _description = 'Fetch External Patient System'

    external_id = fields.Char(required=True)
    system = fields.Selection(selection=[
        ('system_a', 'External System A'),
        ('system_b', 'External System B'),
        ('system_c', 'External System C'),
    ], string="System",required=True)

    def create_records_from_external_data(self):
        # Fetch data from the external system
        external_data = self.fetch_data_from_external_system()

        # Convert data using the adapter
        adapter = ExternalDataAdapter(external_data)
        records = adapter.convert_to_dictionary_format()

        # Create records in `medical.patient`
        for record_data in records:
            record_data['external_system']=self.system
            patient_record = self.env['medical.patient'].sudo().create(record_data)
            return {
                'name':'New Patient',
                'res_model':'medical.patient',
                'type':'ir.actions.act_window',
                'view_mode':'form',
                'view_id':self.env.ref('sdp_hospital.view_medical_patient_form').id,
                'res_id': patient_record.id,
            }

    def fetch_data_from_external_system(self):
        # Dummy XML data for demonstration
        return """
        <patients>
          <patient>
            <patient_name>John Doe</patient_name>
            <patient_age>35</patient_age>
            <patient_diagnosis>Hypertension</patient_diagnosis>
            <email>patient@example.com</email>
            <phone>0700000000</phone>
          </patient>
        </patients>
        """
