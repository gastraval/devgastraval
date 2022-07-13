# Copyright 2021 Studio73 - Iván Pérez <ivan.perez@studio73.es>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    workorder_selectable = fields.Boolean(
        string="Seleccionable para ordenes de trabajo", default=True
    )
