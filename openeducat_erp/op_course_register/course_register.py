from openerp import models, fields,api


class course_register(models.Model):
    _name = 'course.register'
   
    name = fields.Char('Name', size=256)
    parent_id = fields.Many2one('op.parent',"Parent")
    partner_id = fields.Many2one(
        'res.partner', 'Partner', ondelete="cascade")
    payment_id = fields.Many2one('account.payment.term',"Payment Method")
    standard_id = fields.Many2one(
        'op.standard', 'Standard')
    course_id = fields.Many2one('op.course')
    student_id = fields.Many2one('op.student', 'Student')
    state = fields.Selection(
        [('d', 'Draft'), ('s', 'Join'), ('a', 'Accepted'),('i', 'Create Invoice'),
         ('r', 'Rejected')], 'State', default='d')
    class_room = fields.Many2one('op.classroom', "Class Room")
    teacher_id = fields.Many2one('op.faculty',"Teacher In Charge")
    duration = fields.Char("Duration")
    class_status = fields.Selection(
        [('n', 'normal'), ('c', 'Cancelled')],
         'State', default='n')
    total_student = fields.Integer("Total Student",readonly="1")
    invoice_exists = fields.Boolean('Invoice')
    invoice_id = fields.Many2one('account.invoice', "Invoice")
    @api.onchange('student_id')
    
    def onchange_student_id(self):
       
        self.parent_id = self.student_id.parent_id.id
        
    @api.onchange('class_room')
    def onchange_class_room(self):
        self.total_student = self.class_room.capacity
        self.teacher_id = self.class_room.faculty_id.id
        self.duration = self.class_room.course_id.duration
    @api.onchange('standard_id')
    def onchange_standard_id(self):
        self.payment_id = self.standard_id.payment_term.id
        
#     @api.onchange('course_id')
#     def onchange_course_id(self):
#         self.duration = self.course_id.duration
#         self.class_room = self.course_id.class_room.id

    @api.multi
    def act_draft(self):
        self.state = 'd'


    @api.multi
    def act_submit(self):
        self.state = 's'
      
    @api.one
    def act_accept(self):
        self.state = 'a'
        
    @api.one
    def act_reject(self):
        self.state = 'r'
        
    @api.one
    def act_reject(self):
        self.state = 'i'
        
    @api.multi
    def create_invoice(self):
        """ Create invoice for fee payment process of student """

        invoice_pool = self.env['account.invoice']

        default_fields = invoice_pool.fields_get(self)
        invoice_default = invoice_pool.default_get(default_fields)

        for student in self:
            type = 'out_invoice'
            partner_id = student.student_id.partner_id.id
            onchange_partner = invoice_pool.onchange_partner_id(
                type, partner_id)
            invoice_default.update(onchange_partner['value'])

            invoice_data = {
                'partner_id': student.student_id.partner_id.id,
                'course_id': student.course_id.id,
                'date_invoice': fields.Date.today(),
               
            }

        invoice_default.update(invoice_data)
        invoice_id = invoice_pool.create(invoice_default).id
        self.write({'invoice_id': invoice_id, 'invoice_exists': True})
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
            inv_ids = [so.invoice_id.id]
      
             #inv_ids += [invoice.id for invoice in so.invoice_ids]
        # choose the view_mode accordingly
        if len(inv_ids) > 1:
            result['domain'] = \
                "[('id','in',[" + ','.join(map(str, inv_ids)) + "])]"
        else:
            res = self.env.ref('account.invoice_form')
            result['views'] = [(res and res.id or False, 'form')]
            #print inv_ids.id,"----------------"
            result['res_id'] = inv_ids and inv_ids[0] or False
        return result