# -*- coding: utf-8 -*-
{
    'name': "ihfms_hospital",

    'summary': """
            IHFMS Hospital
    """,

    'description': """
        IHFMS Hospital
    """,
    "license": "LGPL-3",
    'author': "Fantastic Four",
    'website': "",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': [
        'contacts',
        'stock',    
    ],

    'data': [
        
        #--------security files--------#
        'security/ir.model.access.csv',
       
        
        #------data files -------#
        'data/sequences.xml',
        'data/email_templates.xml',

        #------report files -------#
 
       
       

        #----wizard files -------#
        
        #--------views--------#
        'views/base/patient.xml',
        'views/base/disease.xml',
        'views/base/health_record.xml',
        'views/base/custom_account.xml',
        'views/base/create_account.xml',
        'views/base/custom_invoice.xml',

        'views/menus.xml',
        
        
       
        
    ],

    "assets": {
        "web.assets_backend": [
            
           
        ],
        "web.assets_qweb": [
        
        ],
        
    },
    
    'images':[
        
    ],
}
