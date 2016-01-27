'''
Created on 24-01-2016

@author: Khai Hoang
'''
from openerp import models, fields, api, _
from openerp.exceptions import Warning


class HrEmpoyee(models.Model):
    _name = 'hr.employee'
    _inherit = 'hr.employee'
