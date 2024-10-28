# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools

class PosMonthlyPaymentsReport(models.Model):
    _name = "report.pos.monthly_payments"
    _description = "Point of Sale Monthly Payments"
    _auto = False
    _order = 'date desc'

    month = fields.Date(string='Month', readonly=True)
    cash_total = fields.Float(string='Cash Total', readonly=True)
    card_total = fields.Float(string='Card Total', readonly=True)
    acc_total = fields.Float(string='Account Total', readonly=True)

    def _select(self):
        return """
            SELECT
                MIN(pos_payment.id) as id,
                DATE_TRUNC('month', pos_payment.create_date AT TIME ZONE 'UTC' AT TIME ZONE 'Australia/Melbourne')::date as month,
                sum(amount) filter (where pos_payment_method.name = 'Cash') as cash_total,
                sum(amount) filter (where pos_payment_method.name = 'Card') as card_total,
                sum(amount) filter (where pos_payment_method.name = 'Customer Account') as acc_total
        """

    def _from(self):
        return """
            FROM pos_payment left join pos_payment_method on pos_payment.payment_method_id = pos_payment_method.id
        """

    def _group_by(self):
        return """
            GROUP BY 2
        """

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
                %s
            )
        """ % (self._table, self._select(), self._from(), self._group_by())
        )
