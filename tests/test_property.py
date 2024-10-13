from odoo.tests.common import TransactionCase

class TestProperty(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestProperty, self).setUp()

        self.property_1_rec = self.env['property'].create({
            'ref':'PROP00010',
            'name':'test',
            'postcode':'123'
        })

    def test_property_1(self):
        property_id = self.property_1_rec

        self.assertRecordValues([property_id], [{
            'ref': 'PROP00010',
            'name': 'test',
            'postcode': '123'
        }])
