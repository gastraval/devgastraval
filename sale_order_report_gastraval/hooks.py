# Copyright 2021 Studio73 - Carlos Reyes <carlos@studio73.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.cr.execute("SELECT * FROM sale_order")
    sales = env.cr.dictfetchall()
    for sale in sales:
        env["sale.order"].browse(sale["id"]).update(
            {
                "delivery_date": sale.get("x_studio_fecha_de_entrega", False),
                "delivery_method": sale.get("x_studio_mtodo_de_entrega", False),
                "total_boxes": sale.get("x_studio_cajas_totales", False),
                "total_tray": sale.get("x_studio_bandejas_totales", False),
                "total_weight": sale.get("x_studio_peso_total", False),
                "observations": sale.get("x_studio_observaciones", False),
                "temperature": sale.get("x_studio_temperatura", False),
            },
        )
