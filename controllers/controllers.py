# -*- coding: utf-8 -*-
from odoo import http

# class SparkitBhc(http.Controller):
#     @http.route('/sparkit_bhc/sparkit_bhc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sparkit_bhc/sparkit_bhc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sparkit_bhc.listing', {
#             'root': '/sparkit_bhc/sparkit_bhc',
#             'objects': http.request.env['sparkit_bhc.sparkit_bhc'].search([]),
#         })

#     @http.route('/sparkit_bhc/sparkit_bhc/objects/<model("sparkit_bhc.sparkit_bhc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sparkit_bhc.object', {
#             'object': obj
#         })