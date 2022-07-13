# Copyright 2022 Studio73 - Ferran Mora <ferran@studio73.es>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    workorder_scan_count_one = fields.Boolean(
        string="Contabilizar una unidad al escanear en órdenes de trabajo",
        help="Al escanear un lote de este producto, si está marcado este campo,"
        " se sumará una unidad en lugar de sumarse la cantidad contenida en el"
        " lote o la demanda.",
    )
