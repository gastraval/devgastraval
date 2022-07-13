# Copyright 2021 Studio73 - Carlos Reyes <carlos@studio73.es>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    products = env["product.template"].search([("default_code", "like", "EL0")])
    for product in products:
        product.update({"is_soup_preparation": True})
