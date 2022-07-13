# Copyright 2021 Studio73 - Carlos Reyes <carlos@studio73.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Stock Picking Report Gastraval",
    "summary": "Crea reportes de resumen de inventadio y crea campos de x_studio",
    "version": "13.0.1.0.0",
    "category": "Stock",
    "author": "Studio73",
    "website": "https://www.studio73.es",
    "license": "LGPL-3",
    "depends": ["stock", "stock_picking_batch"],
    "data": [
        "views/stock_picking.xml",
        "reports/stock_picking_report.xml",
        "reports/stock_picking_templates.xml",
    ],
    "installable": True,
    "external_dependencies": {"python": ["openupgradelib"]},
    "post_init_hook": "post_init_hook",
}
