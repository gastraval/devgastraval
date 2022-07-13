# Copyright 2020 Studio73 - Ioan Galan <ioan@studio73.es>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "MRP Workorder Auto Validate Lot Extension",
    "summary": "Ajustar cantidad lotes a lista materiales en el escaneado",
    "version": "13.0.1.0.0",
    "license": "LGPL-3",
    "author": "Studio73",
    "category": "Manufacturing",
    "website": "https://www.studio73.es",
    "depends": ["mrp_workorder_autovalidate_lot", "mrp_workorder_component_info"],
    "data": ["views/product_views.xml"],
    "installable": True,
}
