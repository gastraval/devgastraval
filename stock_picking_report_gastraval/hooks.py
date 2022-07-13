# Copyright 2021 Studio73 - Carlos Reyes <carlos@studio73.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.cr.execute("SELECT * FROM stock_picking")
    stocks = env.cr.dictfetchall()
    for stock in stocks:
        env["stock.picking"].browse(stock["id"]).update(
            {
                "delivery_date": stock.get("x_studio_fecha_de_entrega", False),
                "delivery_method": stock.get("x_studio_mtodo_de_entrega", False),
                "total_boxes": stock.get("x_studio_cajas_totales", False),
                "total_tray": stock.get("x_studio_bandejas_totales_pedido", False),
            },
        )
