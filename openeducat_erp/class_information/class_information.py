'''
Created on 22-01-2016

@author: Khai Hoang
'''
from openerp.osv import fields,osv
class class_information(osv.osv):
    _name = 'class.information'
    _description = 'Class Information'
    _columns = {
                'name': fields.many2one('class.name','Name'),
                'level': fields.many2one('class.level','Level'),
                'class_subject': fields.many2one('class.subject','Subject'),
                'tutor': fields.many2one('op.faculty','Tutor'),
                'exam_type': fields.many2one('op.exam.type','Exam Type'),
                'session': fields.many2one('class.session','Session'),
                'fee': fields.many2one('class.fee','Fee'),
                }
class_information()
class class_name(osv.osv):
    _name = 'class.name'
    _description = 'Class Name'
    _columns = {
                'name': fields.char('Name',size=128),
                }
class class_session(osv.osv):
    _name = 'class.session'
    _description = 'Class Session'
    _columns = {
                'name': fields.char('Name',size=128),
                }
class class_subject(osv.osv):
    _name = 'class.subject'
    _description = 'Class Subject'
    _columns = {
                'name': fields.char('Name',size=128),
                }
class class_fee(osv.osv):
    _name = 'class.fee'
    _description = 'Class Fee'
    _columns = {
                'name': fields.char('Name',size=128),
                'fee': fields.integer('Fee'),
                }
class_fee()
class class_level(osv.osv):
    _name = 'class.level'
    _description = 'Class Level'
    _columns = {
                'name': fields.char('Name',size=128),
                }
class_level()