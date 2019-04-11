from odoo import http


class Transactions_email(http.Controller):
    @http.route('/transactions/mail/', auth='public')
    def index(self, **kw):
        return 'Ok controller'
