# Copyright 2021 Studio73 - Ethan Hildick <ethan@studio73.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.tests import Form

from odoo.addons.mrp.tests.common import TestMrpCommon


class TestWorkorderCommon(TestMrpCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_4.tracking = "lot"
        cls.lot_1 = cls.env["stock.production.lot"].create(
            {"product_id": cls.product_4.id, "company_id": cls.env.company.id}
        )

    def _create_workorder(self, product_to_build=False, bom=False):
        if not product_to_build:
            product_to_build = self.product_5
        if not bom:
            bom = self.bom_2
        mo_form = Form(self.env["mrp.production"])
        mo_form.product_id = product_to_build
        mo_form.bom_id = bom
        mo_form.product_qty = 100.0
        manufacturing_order = mo_form.save()
        manufacturing_order.action_confirm()
        manufacturing_order.button_plan()
        return manufacturing_order.workorder_ids[0]
