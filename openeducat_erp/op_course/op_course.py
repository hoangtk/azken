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

from openerp import models, fields,api
from datetime import datetime
from datetime import date

class OpCourse(models.Model):
    _name = 'op.course'
    
    course_register_ids = fields.One2many('course.register','course_id',"Course Register")
    invoice_exists = fields.Boolean('Invoice')
    student_sub_lines = fields.Many2many('op.student')
    state = fields.Selection(
        [('d', 'Draft'), ('s', 'Publish'), ('a', 'Accepted'),('i', 'Create Invoice'),
         ('r', 'Rejected')], 'State', default='d')
    discription = fields.Text("Discription")
    school_level = fields.Many2one('op.school.level',"School Level")
    duration = fields.Char("Duration")
    class_room = fields.Many2one('op.classroom', "Class ROom")
    availability = fields.Integer("Avaibality")
    price  = fields.Float("Price")
    quota = fields.Char("Quota")
    teacher_id = fields.Many2one('op.faculty',"Teacher In Charge")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    standard_id = fields.Many2one(
        'op.standard', 'Standard')
    course_uniq_id= fields.Char('ID', size=32, required=True,readonly="1")
    _defaults = {
                'course_uniq_id': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'op.course'),
                }
    name = fields.Char('Name', size=32)
    code = fields.Char('Code', size=8 )
    section = fields.Char('Section', size=32)
    evaluation_type = fields.Selection(
        [('normal', 'Normal'), ('GPA', 'GPA'), ('CWA', 'CWA'), ('CCE', 'CCE')],
        'Evaluation Type')
    payment_term = fields.Many2one('account.payment.term', 'Payment Term')
    subject_ids = fields.Many2many('op.subject', string='Subject(s)')
    admin_created = fields.Boolean('Invoice')
    @api.onchange('class_room')
    def onchange_class_room(self):
        self.availability = self.class_room.availability
        self.teacher_id = self.class_room.faculty_id.id

    @api.multi
    def act_publish(self):
        self.state = 's'

        
        
    @api.multi
    def act_edit(self):
          
        self.state = 'd'
#        
#     @api.one
#     def act_accept(self):
#         self.state = 'a'
#  
#     @api.one
#     def act_reject(self):
#         self.state = 'r'
         
    @api.one
    def act_reject(self):
        self.state = 'i'
class Opschool_level(models.Model):
      _name = 'op.school.level'
      name = fields.Char("Name")
      code = fields.Char("Code")
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
