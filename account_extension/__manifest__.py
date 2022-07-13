# Copyright 2020 Studio73 - Guillermo Llinares <guillermo@studio73.es>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Account Extension",
    "version": "13.0.1.0.0",
    "license": "LGPL-3",
    "author": "Studio73",
    "category": "Invoicing Management",
    "website": "https://www.studio73.es",
    "depends": ["account_payment_partner"],
    "data": [
        "views/account_journal_dashboard_view.xml",
        "views/account_move_view.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
}
