# Copyright 2021 Studio73 - Guillermo Llinares <guillermo@studio73.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    active_waste = fields.Boolean(
        string="Activar mermas",
        help="Si se activa , al fabricar este producto, la cantidad de materiales "
        "a consumir no cambiará en caso de producir más o menos cantidad final.",
    )
    is_soup_preparation = fields.Boolean(string="Product With Soup And Preparation")
    print_box_label = fields.Boolean(string="Print Box Label")
    print_tray_label = fields.Boolean(string="Print Tray Label")
    print_pallet_label = fields.Boolean(string="Print Pallet Label")
