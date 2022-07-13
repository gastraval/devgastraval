# Copyright 2021 Studio73 - Carlos Reyes <carlos@studio73.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Sale Order Report Gastraval",
    "summary": "Crea reportes de pedidos de ventas y crea campos de x_studio",
    "version": "13.0.1.0.0",
    "category": "Stock",
    "author": "Studio73",
    "website": "https://www.studio73.es",
    "license": "LGPL-3",
    "depends": ["sale"],
    "data": [
        "views/sale_order.xml",
        "reports/sale_report.xml",
        "reports/sale_order_templates.xml",
    ],
    "installable": True,
    "external_dependencies": {"python": ["openupgradelib"]},
    "post_init_hook": "post_init_hook",
}
