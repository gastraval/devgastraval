# Copyright 2021 Studio73 - Guillermo Llinares <guillermo@studio73.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, exceptions, fields, models
from odoo.exceptions import UserError


class MrpWorkorder(models.Model):
    _inherit = "mrp.workorder"

    barcode = fields.Char(string="Barcode")
    default_code = fields.Char(string="Default Code", related="product_id.default_code")
    is_soup_preparation = fields.Boolean(
        string="Product With Soup And Preparation",
        related="product_id.is_soup_preparation",
    )
    print_box_label = fields.Boolean(
        string="Print Box Label",
        related="production_id.product_tmpl_id.print_box_label",
    )
    print_tray_label = fields.Boolean(
        string="Print Tray Label",
        related="production_id.product_tmpl_id.print_tray_label",
    )
    production_id = fields.Many2one(index=True)

    def button_start(self):
        if self.workcenter_id.block_same_product:
            same_product_workorders = self.env["mrp.workorder"].search(
                [
                    ("state", "=", "progress"),
                    ("product_id.id", "=", self.product_id.id),
                    ("id", "!=", self.id),
                ]
            )
            if same_product_workorders:
                raise UserError(
                    _("Solo puede haber una orden de trabajo en progreso por producto")
                )
        return super().button_start()

    def action_close(self):
        self.ensure_one()
        self.button_done()
        if all(
            [
                state in ["cancel", "done"]
                for state in self.production_id.workorder_ids.mapped("state")
            ]
        ):
            self.production_id.action_close()
            self.production_id.state = "done"
            return {
                "type": "ir.actions.act_window",
                "res_model": "mrp.production",
                "views": [[self.env.ref("mrp.mrp_production_form_view").id, "form"]],
                "res_id": self.production_id.id,
                "target": "main",
            }
        raise exceptions.UserError(
            _("La orden de producción {} tiene alguna orden de trabajo abierta").format(
                self.production_id.name
            )
        )

    def open_button_pending_wizard(self):
        wizard_view_id = self.env.ref(
            "mrp_extension." "mrp_workorder_employee_record_production_wizard_form"
        )
        return {
            "name": _("Introduzca su identificador de empleado"),
            "res_model": "mrp.workorder.employee.wizard",
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "view_id": wizard_view_id.id,
            "target": "new",
            "context": self.env.context,
        }

    def record_production(self):
        check = (
            self.product_id.print_pallet_label and self.workcenter_id.print_pallet_label
        )
        if check:
            production_move = self.production_id.move_finished_ids.filtered(
                lambda move: move.product_id == self.product_id
                and move.state not in ("done", "cancel")
            )
            finished_lot_id = self.finished_lot_id
        res = super().record_production()
        if check and not self.env.context.get("final_step", False):
            pdf = self._print_pallet_report(production_move, finished_lot_id)
            if pdf:
                pdf["close_on_report_download"] = True
            return pdf
        return res

    def record_production_and_stop(self):
        wizard_view_id = self.env.ref(
            "mrp_extension.mrp_workorder_employee_record_production_wizard_form"
        )
        context = self.env.context.copy()
        context.update(
            {"bypass_update_wo_working_user_code": True, "record_production": True}
        )
        return {
            "name": _("Registrar producción"),
            "res_model": "mrp.workorder.employee.wizard",
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "view_id": wizard_view_id.id,
            "target": "new",
            "context": context,
        }

    def print_label_tray(self):
        self.ensure_one()
        if self.default_code.find("EL0") >= 0 or self.is_soup_preparation:
            wizard_view_id = self.env.ref(
                "mrp_extension.mrp_workorder_tray_report_wizard_view"
            )
            return {
                "name": "Select the tray report type",
                "res_model": "mrp.workorder.tray.report",
                "type": "ir.actions.act_window",
                "view_type": "form",
                "view_mode": "form",
                "view_id": wizard_view_id.id,
                "target": "new",
            }
        else:
            return self.env.ref("mrp_extension.stock_report_lot_tray").report_action(
                self
            )

    def print_label_box(self):
        self.ensure_one()
        return self.env.ref("mrp_extension.stock_report_lot_box").report_action(self)

    def _print_pallet_report(self, move, lot):
        move_line = self.env["stock.move.line"].search(
            [("move_id", "=", move.id), ("lot_id", "=", lot.id)], limit=1
        )
        if move_line:
            pallet = self.env.context.get("package_to_print", False)
            if not pallet:
                pallet = self.env["stock.quant.package"].create({})
            move_line.update({"result_package_id": pallet.id})
            report = self.env["ir.actions.report"].search(
                [
                    ("report_name", "=", "stock.report_package_barcode_copy_1"),
                    ("report_type", "=", "qweb-pdf"),
                ],
                limit=1,
            )
            if report:
                pdf = report.report_action(pallet)
                return pdf
        return False

    def action_open_manufacturing_order(self):
        check = (
            self.product_id.print_pallet_label and self.workcenter_id.print_pallet_label
        )
        if check:
            production_move = self.production_id.move_finished_ids.filtered(
                lambda move: move.product_id == self.product_id
                and move.state not in ("done", "cancel")
            )
            finished_lot_id = self.finished_lot_id
        action = super().action_open_manufacturing_order()
        if check:
            pdf = self._print_pallet_report(production_move, finished_lot_id)
            if pdf:
                pdf["post_action_to_run"] = action
            return pdf
        return action
