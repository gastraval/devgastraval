# Copyright 2021 Studio73 - Carlos Reyes <carlos@studio73.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MrpWorkorderEmployeeWizard(models.TransientModel):
    _name = "mrp.workorder.tray.report"
    _description = "Selector del tipo de reporte de bandeja"

    tray_report_type = fields.Selection(
        string="Tray Report Type",
        selection=[("soup", "Soup Label"), ("preparation", "Preparation Label")],
    )
    workorder_id = fields.Many2one(
        string="Órden de trabajo", comodel_name="mrp.workorder"
    )

    def action_print_tray_label(self):
        self.ensure_one()
        if self.tray_report_type == "preparation":
            return self.env.ref("mrp_extension.stock_report_lot_tray").report_action(
                self.workorder_id
            )
        else:
            return self.env.ref(
                "mrp_extension.stock_report_lot_soup_tray"
            ).report_action(self.workorder_id)
