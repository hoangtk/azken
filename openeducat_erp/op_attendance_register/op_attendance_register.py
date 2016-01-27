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


class OpAttendanceRegister(models.Model):
    _name = 'op.attendance.register'
    
    teacher_id = fields.Many2one('op.faculty',"Teacher In Charge")
    number_of_student = fields.Integer("Number of Student")
    name = fields.Char('Name', size=16, required=True)
    code = fields.Char('Code', size=8)
    course_id = fields.Many2one('op.course', 'Course', required=True)
    batch_id = fields.Many2one('op.batch', 'Batch')
    standard_id = fields.Many2one('op.standard', 'Standard')
    division_id = fields.Many2one('op.division', 'Division')
    subject_id = fields.Many2one('op.subject', 'Subject')
    student_id = fields.Many2one('op.student', 'Student', required=True)
    class_room = fields.Many2one('op.classroom',"Class Room")
    state = fields.Selection(
        [('d', 'Draft'), ('s', 'Submitted'), ('a', 'Accepted'),
         ('r', 'Rejected'), ('c', 'Change Req.')], 'State', default='d')
    status = fields.Selection(
        [('d', 'Present'), ('s', 'Absent'), ('a', 'Sick'),
         ('r', 'Other')])
    comment = fields.Text('Comment')
    active_field = fields.Boolean("Active Field")
    @api.one
    def act_draft(self):
        self.state = 'd'

    @api.one
    def act_submit(self):
        self.state = 's'

    @api.one
    def act_accept(self):
        self.state = 'a'

    @api.one
    def act_reject(self):
        self.state = 'r'
        
    @api.onchange('student_id')
    def onchange_available_class_two(self):
        self.name = self.student_id.name
        self.class_room = self.student_id.class_room.id
        self.course_id = self.student_id.course_id.id
        self.number_of_student = self.class_room.capacity
        self.teacher_id = self.class_room.faculty_id.id

        
#   

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
