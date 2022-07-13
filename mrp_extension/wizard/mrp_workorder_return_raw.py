# Copyright 2022 Studio73 - Ethan Hildick <ethan@studio73.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class MrpWorkorderReturnRaw(models.TransientModel):
    _inherit = "mrp.workorder.return.raw"

    @api.onchange("product_id")
    def _onchange_product_id(self):
        similar_location = self.env["stock.location"]
        if self.product_id:
            category = self.product_id.categ_id
            similar_location = self.env["stock.location"].search(
                [("name", "=", category.name)], limit=1
            )
        self.update({"location_dest_id": similar_location.id})
