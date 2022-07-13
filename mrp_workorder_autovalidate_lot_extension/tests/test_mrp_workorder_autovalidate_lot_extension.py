# Copyright 2021 Studio73 - Carlos Reyes <carlos@studio73.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from .common import TestWorkorderCommon


class TestMrpWorkorderAutovalidateLotExtension(TestWorkorderCommon):
    def test_barcode_scan(self):
        workorder = self._create_workorder()
        workorder.button_start()
        self.lot_2 = self.env["stock.production.lot"].create(
            {"product_id": self.product_4.id, "company_id": self.env.company.id}
        )
        self.env["stock.quant"]._update_available_quantity(
            self.product_4,
            workorder.production_id.location_src_id,
            150,
            lot_id=self.lot_1,
        )
        self.env["stock.quant"]._update_available_quantity(
            self.product_4,
            workorder.production_id.location_src_id,
            200,
            lot_id=self.lot_2,
        )
        workorder.on_barcode_scanned(self.lot_1.name)
        workorder.on_barcode_scanned(self.lot_2.name)
        qty_lot1 = workorder.barcode_lot_line_ids[0].qty_done
        qty_lot2 = workorder.barcode_lot_line_ids[1].qty_done
        real_qty_done = workorder._get_component_remaining_qty(self.lot_1.product_id)
        self.assertEqual(
            real_qty_done, (qty_lot1 + qty_lot2), "Lot quantity is incorrect"
        )
