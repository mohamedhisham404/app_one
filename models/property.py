from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Property(models.Model):
    _name = 'property'
    _description = 'Property' #for the chatter
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(required=True)
    ref = fields.Char(readonly=True,default='New')#for sequence
    description = fields.Text()
    postcode = fields.Char(required=True)
    date_available = fields.Date(tracking=True) #for the chatter
    expected_price = fields.Float()
    selling_price = fields.Float()
    expected_selling_date = fields.Date(tracking=True)
    is_late = fields.Boolean()
    diff = fields.Float(compute='_compute_diff',store=True)
    bedrooms = fields.Integer()
    living_area= fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    orientation = fields.Selection([
        ('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West')
    ], default='north')
    # relation:=> only write in database
    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    state = fields.Selection([
        ('draft','Draft'),
        ('pending','Pending'),
        ('sold','Sold'),
        ('closed','Closed')
    ], default='draft')
    owner_address = fields.Char(related='owner_id.address')
    owner_phone = fields.Char(related='owner_id.phone')

    line_ids = fields.One2many('property.line','property_id')
    active = fields.Boolean(default=True)

    # SQL constraint for uniqueness (optional, can be disabled for testing)
    # _sql_constraints = [
    #     ('name_unique', 'unique(name)', 'Name must be unique')
    # ]

    #logic tier constraints
    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            # Search for other records with the same name excluding the current record
            existing_record = self.search([('name', '=', record.name), ('id', '!=', record.id)])
            if existing_record:
                # raise ValidationError("The name '%s' is already in use. Please choose a different name." % record.name)
                print("i am working")

    #action for button
    def action_draft(self):
        for rec in self:
            rec.create_history_record(rec.state,'draft')
            rec.state = 'draft'


    def action_pending(self):
        for rec in self:
            rec.create_history_record(rec.state,'pending')
            rec.state = 'pending'

    def action_sold(self):
        for rec in self:
            rec.create_history_record(rec.state,'sold')
            rec.state = 'sold'

    def action_closed(self):
        for rec in self:
            rec.create_history_record(rec.state,'closed')
            rec.state = 'closed'

    @api.depends('expected_price', 'selling_price')
    def _compute_diff(self):
        for rec in self:
            rec.diff =  rec.expected_price - rec.selling_price

    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True


    #to write sequence
    @api.model
    def create(self, vals_list):
        res = super(Property,self).create(vals_list)
        if res.ref =="New":
            res.ref = self.env['ir.sequence'].next_by_code('property_sequence')
        return res

    def create_history_record(self,old_state,new_state,reason=""):
        for rec in self:
           rec.env['property.history'].create({
                'user_id': rec.env.uid,
                'property_id': rec.id,
                'old_state': old_state,
                'new_state': new_state,
               'reason': reason or "",
           })

    def action_open_change_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.change_state_wizard_action')
        action['context'] = {'default_property_id':self.id}
        return action

    def action_open_related_owner(self):
        action = self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id= self.env.ref('app_one.owner_view_form').id
        action['res_id'] = self.owner_id.id
        action['views'] = [[view_id,'form']]
        return action

    # @api.model_create_multi #for CRUD operations
    # def create(self, vals_list):
    #     res = super(Property,self).create(vals_list)
    #     #logic
    #     return res
    #
    # @api.model
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None): #read
    #     res = super(Property,self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
    #     # logic
    #     print("i am working")
    #     return res
    #
    # def write(self, vals): #update
    #     res = super(Property, self).write(vals)
    #     # logic
    #     return res
    #
    # def unlink(self):
    #     res = super(Property, self).unlink()
    #     # logic
    #     print("delete working")
    #     return res

    # One2manyLines
class PropertyLine(models.Model):
    _name = 'property.line'

    property_id = fields.Many2one('property')
    area =fields.Float()
    description = fields.Char()
