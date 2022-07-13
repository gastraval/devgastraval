# Copyright 2020 Studio73 - Ethan Hildick <ethan@studio73.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from datetime import date

from odoo import _, api, exceptions, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    def generate_lot_code(self, product):
        return "{}{}".format(
            date.today().strftime("%d%m%y"), product.default_code or ""
        )

    @api.model
    def create(self, vals):
        product = self.env["product.product"].browse(vals["product_id"])
        if product.use_daily_lots:
            lot_code = self.generate_lot_code(product)
            lot_id = (
                self.env["stock.production.lot"]
                .with_context(active_test=False)
                .search(
                    [("name", "=", lot_code), ("product_id", "=", product.id)], limit=1
                )
            )
            if lot_id:
                return lot_id
            else:
                vals["name"] = lot_code
        return super().create(vals)

    @api.constrains("active", "name")
    def _constrain_active_name(self):
        for lot in self:
            if lot.product_id.use_daily_lots:
                lots = self.env["stock.production.lot"].search(
                    [("name", "=", lot.name), ("id", "!=", lot.id)]
                )
                if lots:
                    raise exceptions.ValidationError(
                        _(
                            "Ya existe otro lote activo con el mismo número ({})."
                        ).format(lot.name)
                    )
