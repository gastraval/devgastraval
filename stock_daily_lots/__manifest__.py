# Copyright 2020 Studio73 - Ethan Hildick <ethan@studio73.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Stock Daily Lots",
    "summary": "Usar fecha actual al crear lotes y solo crear uno por día",
    "version": "13.0.1.0.0",
    "category": "Stock",
    "author": "Studio73",
    "website": "https://www.studio73.es",
    "license": "LGPL-3",
    "depends": ["stock", "stock_unique_lot"],
    "data": ["views/product_template_views.xml"],
    "installable": True,
}
