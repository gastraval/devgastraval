# Copyright 2021 Studio73 - Carlos Reyes <carlos@studio73.es>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import _, exceptions, models
from odoo.tools import float_round


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    def _get_lot_lines_by_barcode(self, barcode):
        res = super(MrpWorkorder, self)._get_lot_lines_by_barcode(barcode)
        qty_scanned = 0.0
        for scan in res:
            if scan.get("lot_id"):
                lot = self.env["stock.production.lot"].browse(scan.get("lot_id"))
                if not lot.product_id.workorder_scan_count_one:
                    lot_qty = lot.product_qty
                else:
                    lot_qty = 1
                real_qty_done = self._get_component_remaining_qty_custom(lot.product_id)
                for scanned_lot in self.barcode_lot_line_ids:
                    if lot.product_id.id == scanned_lot.component_id.id:
                        qty_scanned += scanned_lot.qty_done
                qty_done = min(lot_qty, real_qty_done - qty_scanned)
                scan.update({"qty_done": qty_done})
        return res

    def _add_barcode_lot_line(self, vals):
        component_id = self.component_ids.search(
            [
                ("product_id", "=", vals.get("component_id")),
                ("id", "in", self.component_ids.ids),
            ]
        )
        lot_lines_total_qty = sum(
            self.barcode_lot_line_ids.filtered(
                lambda bl: (bl.component_id.id == vals["component_id"])
            ).mapped("qty_done")
        )
        if (component_id.qty_bom - component_id.qty_real) <= lot_lines_total_qty:
            raise exceptions.UserError(_("Has llegado al limite de cantidad"))
        lot = self.env["stock.production.lot"].browse(vals["lot_id"])
        if (
            lot.product_qty
            and sum(
                self.barcode_lot_line_ids.filtered(
                    lambda bl: (bl.lot_id.id == vals["lot_id"])
                ).mapped("qty_done")
            )
            >= lot.product_qty
        ):
            raise exceptions.UserError(_("El lote no tiene suficiente cantidad"))
        if self.barcode_lot_line_ids.filtered(
            lambda bl: (
                not vals.get("package_id")
                and bl.lot_id.id == vals["lot_id"]
                and bl.package_id.id is False
            )
        ):
            self.update({"barcode_lot_line_ids": [(0, 0, vals)]})
        return super()._add_barcode_lot_line(vals)

    def _get_barcode_lot_line_to_validate(self):
        res = super()._get_barcode_lot_line_to_validate()
        lines = []
        for lot_id in list({l["lot"].id for l in res}):
            lot_lines = list(filter(lambda x: x["lot"].id == lot_id, res))
            if len(lot_lines) > 1:
                lines.append(
                    {
                        "component": lot_lines[0]["component"],
                        "lot": lot_lines[0]["lot"],
                        "qty_done": sum(l["qty_done"] for l in lot_lines),
                        "package": lot_lines[0]["package"],
                    }
                )
            else:
                lines.append(lot_lines[0])
        return lines

    def _get_component_remaining_qty_custom(self, component, moves=False):
        if not moves:
            moves = self.component_ids.filtered(lambda m: m.product_id == component)
        if not moves:
            return 0
        return float_round(
            sum(moves.mapped("qty_bom")) - sum(moves.mapped("qty_real")),
            precision_rounding=moves[0].product_id.uom_id.rounding,
        )
