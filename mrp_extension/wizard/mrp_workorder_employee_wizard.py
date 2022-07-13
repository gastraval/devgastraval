# Copyright 2021 Studio73 - Iván Pérez <ivan.perez@studio73.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MrpWorkorderEmployeeWizard(models.TransientModel):
    _name = "mrp.workorder.employee.wizard"
    _description = "Wizard para pedir número de empleado"

    employee_id = fields.Many2one("hr.employee", string="Empleado", required=True)
    workorder_id = fields.Many2one(
        string="Órden de trabajo", comodel_name="mrp.workorder"
    )
    package_id = fields.Many2one(string="Paquete", comodel_name="stock.quant.package")
    print_pallet_label_product = fields.Boolean(string="Print Pallet Label product")
    print_pallet_label_workcenter = fields.Boolean(
        string="Print Pallet Label workcenter"
    )

    @api.model
    def default_get(self, field_list):
        res = super(MrpWorkorderEmployeeWizard, self).default_get(field_list)
        workorder_id = self.env["mrp.workorder"].browse(
            self._context.get("active_ids", [])
        )
        if len(workorder_id) != 1:
            raise UserError(_("Seleccione una única órden de trabajo para registrar"))
        product = workorder_id.product_id
        workcenter = workorder_id.workcenter_id
        res.update(
            {
                "workorder_id": workorder_id.id,
                "print_pallet_label_product": product.print_pallet_label,
                "print_pallet_label_workcenter": workcenter.print_pallet_label,
            }
        )
        return res

    def button_pending(self):
        timeline_obj = self.env["mrp.workcenter.productivity"]
        domain = [
            ("workorder_id", "in", self.workorder_id.ids),
            ("date_end", "=", False),
            ("user_id", "=", self.env.user.id),
        ]
        for timeline in timeline_obj.search(domain, limit=1):
            timeline.write({"employee_id": self.employee_id.id})
        return self.workorder_id.button_pending()

    def record_production(self):
        self.button_pending()
        return self.workorder_id.with_context(
            package_to_print=self.package_id
        ).record_production()

    def action_open_manufacturing_order(self):
        self.button_pending()
        return self.workorder_id.with_context(
            package_to_print=self.package_id, final_step=True
        ).action_open_manufacturing_order()
