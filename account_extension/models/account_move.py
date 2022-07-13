# Copyright 2020 Studio73 - Guillermo Llinares <guillermo@studio73.es>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def unlink(self):
        return super(AccountMove, self.with_context(force_delete=True)).unlink()

    def create(self, vals):
        if self.env.context.get("active_model") == "sale.order" and vals.get(
            "invoice_partner_bank_id", False
        ):
            invoice_partner_bank_id = vals["invoice_partner_bank_id"]
            move = super().create(vals)
            move.update({"invoice_partner_bank_id": invoice_partner_bank_id})
            return move
        return super().create(vals)
