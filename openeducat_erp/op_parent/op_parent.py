# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class OpParent(models.Model):
    _name = 'op.parent'
    
    _defaults = {
                'parents_uniq_id': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'op.parent'),
                }
    account_parent_id = fields.Many2one('account.account',"Account Number")
    parents_uniq_id = fields.Char("Parents Uniq Id",size=128)
    street = fields.Char("City",size=256)
    street2 = fields.Char("City",size=256)
    zip= fields.Integer("City",size=256)
    city = fields.Char("City",size=256)
    country_id = fields.Many2one('res.country',"Country")
    mobile_number = fields.Char("Mobile Number",size=256)
    home_number = fields.Char("Home Number",size=256)
    birth_date = fields.Date('Birth Date')
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female'),
        ], 'Gender')
    email = fields.Char('Email', size=128)
    name = fields.Char('Parent Name')
    nric= fields.Char('NRIC', size=128)
    photo = fields.Binary('Photo')
    relationship_id = fields.Many2one("relationship","Relations Ship")
    
    
    #name = fields.Many2one('res.partner', 'Parent Name', required=True)
    student_ids = fields.Many2many('op.student', string='Select Student')
    user_id = fields.Many2one('res.users', 'User', required=True)
    is_admin_group = fields.Boolean(compute='_is_read_group')
    password = fields.Char('Password')
    def _is_read_group(self):
        flag = self.env['res.users'].has_group('openeducat_erp.group_op_back_office_admin') 
        self.is_admin_group = flag
    @api.multi
    def write(self, values):
        result = super(OpParent,self).write(values)
        if values.get('password') != '':
            roots = self.search([('id','in',self.ids)])
            roots.user_id.password = values.get('password')
        return result            
class relationship(models.Model):
        _name = 'relationship'
        
        name = fields.Char("Relation")
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
