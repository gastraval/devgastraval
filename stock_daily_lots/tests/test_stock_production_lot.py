# Copyright 2020 Studio73 - Ethan Hildick <ethan@studio73.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.addons.stock.tests.common import TestStockCommon


class TestStockProductionLot(TestStockCommon):
    def test_create(self):
        self.productA.write({"tracking": "lot", "use_daily_lots": True})
        lot1 = self.LotObj.create(
            {"product_id": self.productA.id, "company_id": self.env.company.id}
        )
        lot2 = self.LotObj.create(
            {"product_id": self.productA.id, "company_id": self.env.company.id}
        )
        self.assertEqual(
            lot1.id,
            lot2.id,
            "Al ser del mismo dia y mismo producto, deberia de usarse el mismo lote",
        )
        lot3 = self.LotObj.create(
            {"product_id": self.productB.id, "company_id": self.env.company.id}
        )
        self.assertNotEqual(
            lot1.id,
            lot3.id,
            "Al ser productos diferentes deberia de crear un nuevo lote",
        )
