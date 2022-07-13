# Copyright 2022 Studio73 - Ethan Hildick <ethan@studio73.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    department = env["hr.department"].search([("name", "=", "PRODUCCIÓN")], limit=1)
    if department:
        openupgrade.add_xmlid(
            env.cr,
            "mrp_extension",
            "hr_department_production",
            "hr.department",
            department.id,
            noupdate=True,
        )
