from odoo import fields, models


class WorkersAttendance(models.Model):
    _name = 'workers.attendance'
    _description = 'Workers attendance module'

    tag_id = fields.Char('Tag id', readonly=True)
    name = fields.Many2one('res.partner', 'Name', readonly=True)
    rfid_status = fields.Boolean('Status',
                                 help='If checkbox is checked it means worker has entered. Otherwise - exited.',
                                 readonly=True)
