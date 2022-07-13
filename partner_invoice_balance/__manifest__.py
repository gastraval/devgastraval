# Copyright 2020 Studio73 - Abraham Anes <abraham@studio73.es>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Partner Invoice Balance",
    "summary": "Permite pasar el saldo de facturas "
    "de proveedor a la cuenta del cliente",
    "version": "13.0.1.0.0",
    "license": "LGPL-3",
    "author": "Studio73",
    "category": "Invoicing Management",
    "website": "https://www.studio73.es",
    "depends": ["account"],
    "data": [
        "views/account_move_view.xml",
        "views/res_config_settings_view.xml",
        "views/res_partner_view.xml",
    ],
    "installable": True,
}
