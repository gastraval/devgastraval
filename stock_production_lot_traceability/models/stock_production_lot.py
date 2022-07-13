# Copyright 2021 Studio73 - Ferran Mora <ferran@studio73.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    def action_lot_open_move_lines(self):
        lot_list = self._get_lot_traceability_domain(self.id)
        return self.env["stock.production.lot"]._get_lot_traceability_action(
            [("id", "in", lot_list), ("active", "in", [True, False])]
        )

    def _get_lot_traceability_action(self, domain):
        action = self.env.ref("stock.action_production_lot_form").read()[0]
        action["domain"] = domain
        return action

    def _get_lot_traceability_domain(self, lot_id):
        move_lines = (
            self.env["stock.move.line"]
            .with_context(active_test=False)
            .search([("lot_id", "=", lot_id)])
        )
        next_lots = move_lines.mapped("lot_produced_ids.id")
        lot_list = []
        for lot in next_lots:
            lot_list.extend(self._get_lot_traceability_domain(lot))
        lot_list.extend(next_lots)
        return lot_list
