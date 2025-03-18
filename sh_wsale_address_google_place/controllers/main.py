# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import Controller, request, route

class CustomController(http.Controller):

    @http.route(['/sh_get_google_api_key'], type='json', auth="public", website=True)
    def sh_get_google_api_key(self, **post):
        Website = request.env['website']
        api_key = False
        website_api_key = Website.get_current_website().google_maps_api_key
        if website_api_key:
            api_key = website_api_key
        return {'api_key':api_key}

    @http.route(['/sh_get_country_state_code'], type='json', auth="public", website=True)
    def sh_get_country_state_code(self,country_name='',state_name='', **post):
        country_name = country_name or ''
        state_name = state_name or ''
        code = ''
        
        country_code = request.env["res.country"].sudo().search([('name','=',country_name)],limit=1)
        if country_code:
            code = country_code.id if country_code else ''
        
        state_code = request.env["res.country.state"].sudo().search([('name','=',state_name)],limit=1)
        if state_code:
            state_code = state_code.id if state_code else ''
        
        return {'country_code':code,'state_code':state_code}
    
class CustomerPortal(CustomerPortal):
    
    @route()
    def account(self, redirect=None, **post):
        if post.get('address'):
            del post['address']
        return super().account(redirect=redirect,**post)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    