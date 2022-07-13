# Copyright 2021 Studio73 - Guillermo Llinares <guillermo@studio73.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, models


class MrpAbstractWorkorder(models.AbstractModel):
    _inherit = "mrp.abstract.workorder"

    @api.model
    def _prepare_component_quantity(self, move, qty_producing):
        if self.production_id.active_waste:
            return move.product_qty
        return super(MrpAbstractWorkorder, self)._prepare_component_quantity(
            move, qty_producing
        )
