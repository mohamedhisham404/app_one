# TODO:not working
import json
from odoo import http
from odoo.http import request

# class PropertyApi(http.Controller):
#     @http.route('/api/properties', methods=["POST"],type='http', auth='none',csrf=False)
#     def post_properties(self):
#         args = request.httprequest.data.decode()
#         vals = json.loads(args)
#         res = request.env['property'].sudo().create(vals)
#         if res:
#             return request.make_json_response({
#                 "message":'success'
#             },status=200)




class Test(http.Controller):
    @http.route("/api/test", methods=["GET"], type="http", auth="none", csrf=False)
    def test(self):
        return http.Response('{"message": "Test successful"}', content_type='application/json')

