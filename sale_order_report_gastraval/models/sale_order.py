# Copyright 2021 Studio73 - Carlos Reyes <carlos@studio73.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    delivery_date = fields.Date(string="Fecha de entrega")
    delivery_method = fields.Char(string="Transportista")
    total_boxes = fields.Float(string="Cajas totales")
    total_tray = fields.Float(string="Bandejas totales")
    total_weight = fields.Float(string="Peso total")
    observations = fields.Text(string="Observaciones")
    temperature = fields.Char(string="Temperatura")
