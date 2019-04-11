from odoo import http

#responde a http://localhost:8069/transactions/mail
class Transactions_email(http.Controller):
    @http.route('/transactions/mail/', auth='public')
    def index(self, **kw):
        return http.request.render(
            'transactions_email.index',
            {
                "list_email": [
                    "arithgrey@gmail.com",
                    "enidservive@gmail.com",
                    "jonathan.medrano@benandfrank.com",
                ]
            }
        )
