from openerp import models, fields,api

class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line' 
    course_product_id = fields.Many2one('op.course',"Class List")
    
    @api.onchange('course_product_id')
    def onchange_course_product_id(self):
            self.price_unit = self.course_product_id.price
            
class account_invoice(models.Model):
    _inherit = 'account.invoice'
   
    school_level = fields.Many2one('op.school.level',"School Level")
    course_id = fields.Many2one('op.course',"Class ID")
    
    student_id = fields.Many2one('op.student',"Student")
    parent_id = fields.Many2one('op.parent',"Parent")
    payment_id = fields.Many2one('account.payment.term')
    standard_id = fields.Many2one(
        'op.standard', 'Standard')
    class_name = fields.Char('Class Name')
    teacher_id = fields.Many2one('op.faculty',"Teacher")
    duration = fields.Char('Duration')
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    
    @api.onchange('student_id')
    def onchange_student_id(self):
            self.standard_id = self.student_id.standard_id.id
            self.parent_id = self.student_id.parent_id.id
            
    @api.onchange('course_id')
    def onchange_course_id(self):
            self.class_name = self.course_id.name
            self.start_date = self.course_id.start_date
            self.end_date = self.course_id.end_date
            self.school_level = self.course_id.school_level.id
            self.duration = self.course_id.duration
            self.teacher_id = self.course_id.teacher_id.id
            i_obj = self.pool.get('account.invoice.line')

#             acc_invs = self.env['account.invoice.line'].browse(
#             self.env.context.get('active_ids', False))
#             print acc_invs,"============>>>>"
            

               
    @api.onchange('standard_id')
    def onchange_standard_id(self):
            self.payment_id = self.standard_id.payment_term.id
            

   