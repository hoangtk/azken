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


class OpClassroom(models.Model):
    _name = 'op.classroom'

    list_class_room = fields.Many2one("op.classroom","List of Class")
    class_type = fields.Many2one("op.classtype","Class Type")
    faculty_id = fields.Many2one('op.faculty', 'Teacher In Charge')
    category = fields.Many2one(
        'op.category', 'Category')
    name = fields.Char('Name', size=16,)
    code = fields.Char('Code', size=4)
    subject = fields.Many2one('op.subject', 'Subject')
    course_id = fields.Many2one('op.course', 'Course')
    standard_id = fields.Many2one('op.standard', 'Standard')
    capacity = fields.Integer(string='Capacity')
    availability = fields.Integer(compute = '_get_room_seat',string ="Availability")
    facility = fields.Many2many('op.facility', string='Facilities')
    
    combine_id = fields.Many2one('op.classcombine',"Combine")
    asset_line = fields.One2many(
        'op.asset', 'asset_id', 'Asset')

    @api.multi
    def _get_room_seat(self):
        print "ddd"


        student_obj = self.env['op.student']
#         for rec in self:
#             ids_s = student_obj.search([('class_room','=', rec.id)])
#             rec.availability = rec.capacity - ids_s.__len__() 
        count_list = 0  
        for rec in self:
            st_ids = student_obj.search([])
            for data in st_ids:
                for c_id in data.course_ids:
                    if c_id.class_room.id == rec.id:
                        count_list = count_list+1
        rec.availability = rec.capacity - count_list
               
                #print data.course_ids,"xxxxx"
#                 for c in data.course_ids:
#                     print "====",c.id
#             ids_s = student_obj.search([('class_room','=', rec.id)])
            
            #rec.availability = rec.capacity - ids_s.__len__()           
           
class OpAsset(models.Model):
    _name = 'op.asset'

    asset_id = fields.Many2one('op.classroom', 'Asset')
    product_id = fields.Many2one('product.product', 'Product')
    code = fields.Char('Code', size=256)
    product_uom_qty = fields.Float('Quantity')
    
class OpClassType(models.Model):
    _name = 'op.classtype'
    name = fields.Char('Name')
    code = fields.Char('Code')
    
class OpClassCombine(models.Model):
    _name = 'op.classcombine'

    
    available_class = fields.Many2one("op.classroom","Available Class One")
    available_class_two = fields.Many2one("op.classroom","Available Class Two")
    
    available_seat = fields.Integer('Seat Available')
    available_seat_two = fields.Integer('Seat Available')
    total_seat_available = fields.Integer("Total Seat Available")
    combine_class_ids = fields.One2many('op.classroom','combine_id',"Create New Class")
    sync_data = fields.Boolean("Active", default = False)
    classroom_id = fields.Many2one('op.classroom',"Class Room")
    faculty_id = fields.Many2one('op.faculty', 'Teacher In Charge')

    @api.onchange('total_seat_available')
    def onchange_total_seat(self):
        print "call on change"
        
        for rec in self.combine_class_ids:
            rec.course_id = self.course_id
#         res = {'value': {}}
#         
#         for rec in self.browse(cr,uid,ids,context=context):
#             
#             res['value'] = {'course_id':rec.available_class.course_id}
#             print res,"222222222"

    def create_combine_class(self, cr, uid, ids, context=None):
          
          
          
        class_room_obj = self.pool.get('op.classroom')
          
        res = {}
          
         
          
       
        class_id = False
        for rec in self.browse(cr,uid,ids,context=context):
            if rec.total_seat_available < rec.available_class.capacity:
               class_id = class_room_obj.create(cr, uid,{'name' :rec.available_class.name + " / " + rec.available_class_two.name,
                                                  'subject' : rec.available_class.subject.id,
                                                  'class_type' : rec.available_class.class_type.id,
                                                  'course_id': rec.available_class.course_id.id,
                                                  'category': rec.available_class.category.id,
                                                  'faculty_id': rec.available_class.faculty_id.id,
                                                  'capacity': rec.total_seat_available,
                                                  'availability': rec.total_seat_available,
                                                   'combine_id': class_id,
                                                  }, context=None)
                 
               rec.sync_data = True
               
        return res
        
        

       
    
    @api.onchange('available_class')
    def onchange_available_class(self):
        self.available_seat = self.available_class.availability
        self.total_seat_available = self.available_seat + self.available_seat_two
        
    @api.onchange('available_class_two')
    def onchange_available_class_two(self):
    
        self.available_seat_two = self.available_class_two.availability
        self.total_seat_available = self.available_seat_two + self.available_seat
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
