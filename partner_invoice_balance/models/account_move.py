# Copyright 2020 Studio73 - Abraham Anes <abraham@studio73.es>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import _, fields, models
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    transfer_invoice_balance = fields.Boolean(
        string="Trasladar saldos desde factura",
        related="partner_id.transfer_invoice_balance",
    )

    def action_transfer_invoice_balance(self):
        for move in self:
            if (
                move.state != "posted"
                or move.invoice_payment_state != "not_paid"
                or move.type != "in_invoice"
                or not move.transfer_invoice_balance
            ):
                continue
            if not move.company_id.transfer_invoice_balance_journal_id:
                raise UserError(
                    _("Debe configurar un diario para traspasos a la cuenta cliente")
                )
            journal = move.company_id.transfer_invoice_balance_journal_id
            invoice_ml = self.line_ids.filtered(
                lambda mline: mline.account_id.user_type_id.type == "payable"
                and mline.credit > 0
            )
            new_ref = "Traspaso a cuenta de factura {}".format(move.name)
            move_line_vals = [
                {
                    "name": new_ref,
                    "debit": 0,
                    "credit": move.amount_total,
                    "quantity": 1.0,
                    "currency_id": move.currency_id.id
                    if move.currency_id != move.company_id.currency_id
                    else False,
                    "account_id": move.partner_id.property_account_receivable_id.id,
                    "partner_id": move.partner_id.id,
                    "exclude_from_invoice_tab": True,
                },
                {
                    "name": new_ref,
                    "debit": move.amount_total,
                    "credit": 0,
                    "quantity": 1.0,
                    "currency_id": move.currency_id.id
                    if move.currency_id != move.company_id.currency_id
                    else False,
                    "account_id": invoice_ml.account_id.id,
                    "partner_id": move.partner_id.id,
                    "exclude_from_invoice_tab": True,
                },
            ]
            transfer_move = self.env["account.move"].create(
                {
                    "type": "entry",
                    "journal_id": journal.id,
                    "ref": new_ref,
                    "line_ids": [(0, 0, m_vals) for m_vals in move_line_vals],
                }
            )
            transfer_move.action_post()
            new_debit_ml = transfer_move.line_ids.filtered(lambda mline: mline.debit)
            (invoice_ml | new_debit_ml).reconcile()
        return True
