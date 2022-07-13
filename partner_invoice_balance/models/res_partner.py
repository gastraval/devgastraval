# Copyright 2020 Studio73 - Abraham Anes <abraham@studio73.es>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    transfer_invoice_balance = fields.Boolean(
        string="Trasladar saldos desde factura",
        default=False,
        track_visibility="onchange",
    )
