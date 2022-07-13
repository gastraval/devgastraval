# Copyright 2021 Studio73 - Carlos Reyes <carlos@studio73.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "stock.picking"

    delivery_date = fields.Date(string="Fecha de entrega")
    delivery_method = fields.Char(string="Método de entrega")
    total_boxes = fields.Float(string="Cajas totales")
    total_tray = fields.Float(string="Bandejas totales")
