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

class OpStudent(models.Model):
    _name = 'op.student'
    _inherits = {'res.partner': 'partner_id'}

    @api.depends('roll_number_line', 'roll_number_line.roll_number',
                 'roll_number_line.student_id', 'roll_number_line.standard_id',
                 'roll_number_line.standard_id.sequence')
    
    def _get_curr_roll_number(self):
        #         for student in self:
        roll_no = 0
        seq = 0
        for roll_number in self.roll_number_line:
            if roll_number.standard_id.sequence > seq:
                roll_no = roll_number.roll_number
                seq = roll_number.standard_id.sequence
        self.roll_number = roll_no
        
    _defaults = {
                'student_uniq_id': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'op.student'),
                }
    
    course_id = fields.Many2one('op.course',"Course")
    account_stduent_id = fields.Many2one('account.account',"Account Number")
    student_uniq_id = fields.Char("Student Uniq Id",size=128)
    class_room = fields.Many2one('op.classroom',"Class Room")
    partner_bank_id = fields.Many2one('res.partner.bank',"Bank Account Name") 
    account_name = fields.Char("Account Name",size=128)
    school_name = fields.Char("Name of school",size=128) 
    mobile_number = fields.Char("Mobile Number",size=256)
    home_number = fields.Char("Home Number",size=256)
    nric= fields.Char('NRIC', size=128)
    paypal_detail = fields.Text("Paypal Information")
    
    middle_name = fields.Char('Middle Name', size=128)
    last_name = fields.Char('Middle Name', size=128)
    birth_date = fields.Date('Birth Date')
    blood_group = fields.Selection(
        [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
         ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
        'Blood Group')
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female')], 'Gender')
    nationality = fields.Many2one('res.country', 'Nationality')
    language = fields.Many2one('res.lang', 'Mother Tongue')
    category = fields.Many2one(
        'op.category', 'Category')
    religion = fields.Many2one('op.religion', 'Religion')
    library_card = fields.Char('Library Card', size=64)
    emergency_contact = fields.Many2one(
        'res.partner', 'Emergency Contact')
    pan_card = fields.Char('PAN Card', size=64)
    bank_acc_num = fields.Char('Bank Acc Number', size=64)
    visa_info = fields.Char('Visa Info', size=64)
    id_number = fields.Char('ID Card Number', size=64)
    photo = fields.Binary('Photo')
    course_id = fields.Many2one('op.course', 'Course')
    course_ids = fields.Many2many('op.course',string= 'Course')
    division_id = fields.Many2one('op.division', 'Division')
    batch_id = fields.Many2one('op.batch', 'Batch')
    standard_id = fields.Many2one(
        'op.standard', 'Standard')
    roll_number_line = fields.One2many(
        'op.roll.number', 'student_id', 'Roll Number')
    partner_id = fields.Many2one(
        'res.partner', 'Partner', ondelete="cascade")
    health_lines = fields.One2many('op.health', 'student_id', 'Health Detail')
    roll_number = fields.Char(
        'Current Roll Number', compute='_get_curr_roll_number',
        size=8, store=True)
    allocation_ids = fields.Many2many('op.assignment', string='Assignment')
    alumni_boolean = fields.Boolean('Alumni Student')
    passing_year = fields.Many2one('op.batch', 'Passing Year')
    current_position = fields.Char('Current Position', size=256)
    current_job = fields.Char('Current Job', size=256)
    email = fields.Char('Email', size=128)
    phone = fields.Char('Phone Number', size=256)
    user_id = fields.Many2one('res.users', 'Login User',required=True)
    placement_line = fields.One2many(
        'op.placement.offer', 'student_id', 'Placement Details')
    activity_log = fields.One2many(
        'op.activity', 'student_id', 'Activity Log')
    parent_id = fields.Many2one('op.parent', string='Parent')
    parents_uniq_id = fields.Char(string='Parent Id',
                               related='parent_id.parents_uniq_id',readonly=True) 
    gr_no = fields.Char("GR Number", size=20)
    invoice_exists = fields.Boolean('Invoice')
    class_infors = fields.Many2many('class.information',
                                    string='Class Information')
    is_admin_group = fields.Boolean(compute='_is_read_group')
    password = fields.Char('Password')
    def _is_read_group(self):
        flag = self.env['res.users'].has_group('openeducat_erp.group_op_back_office_admin') 
        self.is_admin_group = flag
    @api.constrains('user_id')
    def _check_student_user_id(self):
        all_tt_ids = self.search([])
        for a in all_tt_ids:
            if a.id == self.id:
                return True
            if self.user_id.id == a.user_id.id:
                raise Exception(
                    _("User Already Exist"))
    @api.multi
    def write(self, values):
        result = super(OpStudent,self).write(values)
        if values.get('password') != '':
            roots = self.search([('id','in',self.ids)])
            roots.user_id.password = values.get('password')
        return result
    @api.multi
    def create_invoice(self):
        """ Create invoice for fee payment process of student """

        invoice_pool = self.env['account.invoice']

        default_fields = invoice_pool.fields_get(self)
        invoice_default = invoice_pool.default_get(default_fields)

        for student in self:
            type = 'out_invoice'
            partner_id = student.partner_id.id
            onchange_partner = invoice_pool.onchange_partner_id(
                type, partner_id)
            invoice_default.update(onchange_partner['value'])

            invoice_data = {
                'partner_id': student.partner_id.id,
                'date_invoice': fields.Date.today(),
                'payment_term': student.standard_id.payment_term,
            }

        invoice_default.update(invoice_data)
        invoice_id = invoice_pool.create(invoice_default).id
        self.write({'invoice_ids': [(4, invoice_id)], 'invoice_exists': True})
        form_view = self.env.ref('account.invoice_form')
        tree_view = self.env.ref('account.invoice_tree')
        value = {
            'domain': str([('id', '=', invoice_id)]),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice',
            'view_id': False,
            'views': [(form_view and form_view.id or False, 'form'),
                      (tree_view and tree_view.id or False, 'tree')],
            'type': 'ir.actions.act_window',
            'res_id': invoice_id,
            'target': 'current',
            'nodestroy': True
        }
        return value

    @api.multi
    def action_view_invoice(self):
        '''
        This function returns an action that
        display existing invoices of given student ids and show a invoice"
        '''
        result = self.env.ref('account.action_invoice_tree1')
        id = result and result.id or False
        result = self.env['ir.actions.act_window'].browse(id).read()[0]
        # compute the number of invoices to display
        inv_ids = []
        for so in self:
            
            inv_ids += [invoice.id for invoice in so.invoice_ids]
        
        # choose the view_mode accordingly
        if len(inv_ids) > 1:
            result['domain'] = \
                "[('id','in',[" + ','.join(map(str, inv_ids)) + "])]"
        else:
            res = self.env.ref('account.invoice_form')
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = inv_ids and inv_ids[0] or False
        return result

class OpCourse(models.Model):
    _inherit = 'op.course'
    
    student_id = fields.Many2one('op.student',"Student")
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
