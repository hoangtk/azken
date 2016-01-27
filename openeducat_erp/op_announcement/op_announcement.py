from openerp import models, fields, api


class op_announcement(models.Model):
    _name = 'op.announcement'
    
    announcement_id = fields.Char("ID", readonly="1")
    title = fields.Char("Title")
    message = fields.Text("Message")
    post_to = fields.Selection(
        [('e', 'Email Blast'), ('h', 'Home Page Banner')], 'Post To')
    
    
    _defaults = {
                'announcement_id': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid, 'op.announcement'),
                }