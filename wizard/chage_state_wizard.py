from odoo import fields ,models

class ChangeState(models.TransientModel):
    _name = 'change.state'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending')
        ], default='draft')
    property_id = fields.Many2one('property')
    reason = fields.Char()

    def action_confirm(self):
        if self.property_id.state =='closed':
            self.property_id.state = self.state
            self.property_id.create_history_record('closed',self.state,self.reason)

