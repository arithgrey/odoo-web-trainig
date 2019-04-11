from odoo import api, models, fields


class Transactions_email(models.Model):
    _name = 'transactions.email'
    name = fields.Char()
    