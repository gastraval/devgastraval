# Copyright 2021 Studio73 - Iván Pérez <ivan.perez@studio73.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MrpWorkcenter(models.Model):
    _inherit = "mrp.workcenter"

    block_same_product = fields.Boolean(
        string="Bloquear ordenes de trabajo", default=True,
    )
    print_pallet_label = fields.Boolean(string="Print Pallet Label")


class MrpWorkcenterProductivity(models.Model):
    _inherit = "mrp.workcenter.productivity"

    employee_id = fields.Many2one("hr.employee", string="Empleado")
