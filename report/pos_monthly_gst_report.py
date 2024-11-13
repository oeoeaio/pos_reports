# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools

class PosMonthlyGSTReport(models.Model):
    _name = "report.pos.monthly_gst"
    _description = "Point of Sale Monthly GST"
    _auto = False
    _order = 'date desc'

    month = fields.Date(string='Order Month', readonly=True)
    pos_config_name = fields.Char(string='POS Config Name', readonly=True)
    gst_total = fields.Float(string='GST Total', readonly=True)

    def _select(self):
        return """
            SELECT
                MIN(pos_order.id) as id,
                DATE_TRUNC('month', pos_order.create_date AT TIME ZONE 'UTC' AT TIME ZONE 'Australia/Melbourne')::date as month,
                pos_config.name pos_config_name,
                sum(pos_order.amount_tax) as gst_total
        """

    def _from(self):
        return """
            FROM pos_order
            LEFT JOIN pos_session on pos_session.id = pos_order.session_id
            LEFT JOIN pos_config on pos_config.id = pos_session.config_id
        """

    def _where(self):
        return """
            WHERE pos_order.state = 'done'
        """

   # This is magic
    def _group_by(self):
        return """
            GROUP BY 2,3
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
