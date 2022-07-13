# Copyright 2020 Studio73 - Abraham Anes <abraham@studio73.es>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    transfer_invoice_balance_journal_id = fields.Many2one(
        comodel_name="account.journal",
        string="Diario de traslado de saldo a cliente",
        related="company_id.transfer_invoice_balance_journal_id",
        readonly=False,
    )
