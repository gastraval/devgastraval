# Copyright 2021 Studio73 - Guillermo Llinares <guillermo@studio73.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    active_waste = fields.Boolean(
        string="Activar mermas",
        help="Si se activa la cantidad de materiales a consumir no cambiará en caso "
        "de producir más o menos cantidad final.",
    )

    @api.onchange("product_id", "picking_type_id", "company_id")
    def onchange_product_id(self):
        self.active_waste = self.product_id.active_waste
        return super(MrpProduction, self).onchange_product_id()

    def _update_raw_move(self, bom_line, line_data):
        self.ensure_one()
        if self.active_waste:
            # No actualizar cantidades de move_raw_ids al producir
            # más cantidad de la planeada
            return
        return super(MrpProduction, self)._update_raw_move(bom_line, line_data)

    @api.model
    def create(self, vals):
        if "product_id" in vals:
            product_id = self.env["product.product"].browse([vals["product_id"]])
            vals.update({"active_waste": product_id.active_waste})
        return super(MrpProduction, self).create(vals)
