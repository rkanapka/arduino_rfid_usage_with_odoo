from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    tag_id = fields.Char('Tag id')
