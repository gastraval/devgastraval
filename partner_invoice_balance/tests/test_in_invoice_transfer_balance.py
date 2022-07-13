# Copyright 2020 Studio73 - Abraham Anes <abraham@studio73.es>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.exceptions import UserError

from odoo.addons.account.tests.account_test_savepoint import AccountTestInvoicingCommon


class TestInInvoiceTransferBalance(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        self = cls

        self.invoice = self.init_invoice("in_invoice")
        self.invoice.action_post()
        self.invoice.partner_id.transfer_invoice_balance = True

    def test_action_transfer_invoice_balance(self):
        with self.assertRaises(UserError), self.cr.savepoint():
            self.invoice.action_transfer_invoice_balance()

        journal = self.env["account.journal"].create(
            {
                "name": "Transfer Journal",
                "code": "TTJ",
                "type": "general",
                "company_id": self.env.user.company_id.id,
            }
        )
        self.invoice.company_id.transfer_invoice_balance_journal_id = journal.id
        self.invoice.action_transfer_invoice_balance()
        self.assertEqual(self.invoice.invoice_payment_state, "paid")
