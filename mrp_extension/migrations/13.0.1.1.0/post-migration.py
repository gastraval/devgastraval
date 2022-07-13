# Copyright 2021 Studio73 - Carlos Reyes <carlos@studio73.es>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    env.cr.execute("SELECT * FROM mrp_workorder")
    workorders = env.cr.dictfetchall()
    for workorder in workorders:
        query = "UPDATE mrp_workorder SET barcode = %s WHERE id = %s"
        env.cr.execute(
            query, [workorder.get("x_studio_cdigo_de_barras", False), workorder["id"]]
        )
    env.cr.execute("SELECT * FROM product_product")
    lots = env.cr.dictfetchall()
    for lot in lots:
        env["stock.production.lot"].browse(lot["id"]).update(
            {"barcode": lot.get("x_studio_barcode", False)},
        )
