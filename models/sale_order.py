from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    property_id = fields.Many2one('property')

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        return res