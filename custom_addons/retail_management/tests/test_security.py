from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestRetailSecurity(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cashier = cls.env["res.users"].create(
            {
                "name": "Test Cashier",
                "login": "rms_cashier",
                "group_ids": [(6, 0, [cls.env.ref("retail_management.group_retail_cashier").id])],
            }
        )
        cls.manager = cls.env["res.users"].create(
            {
                "name": "Test Manager",
                "login": "rms_manager",
                "group_ids": [(6, 0, [cls.env.ref("retail_management.group_retail_manager").id])],
            }
        )
        cls.product = cls.env["product.product"].create(
            {"name": "Security Test Product", "list_price": 10.0, "available_in_pos": True, "is_storable": True}
        )
        config = cls.env["pos.config"].create({"name": "Security Test Shop"})
        cls.session = cls.env["pos.session"].create(
            {"config_id": config.id, "user_id": cls.manager.id}
        )
        cls.order = cls.env["pos.order"].create(
            {
                "session_id": cls.session.id,
                "amount_total": 0.0,
                "amount_tax": 0.0,
                "amount_paid": 0.0,
                "amount_return": 0.0,
            }
        )

    # --- denied operations -------------------------------------------------
    def test_cashier_cannot_create_product(self):
        with self.assertRaises(AccessError):
            self.env["product.product"].with_user(self.cashier).create({"name": "Nope"})

    def test_cashier_cannot_write_stock_quant(self):
        quant = self.env["stock.quant"].create(
            {"product_id": self.product.id, "location_id": self.env.ref("stock.stock_location_stock").id}
        )
        with self.assertRaises(AccessError):
            quant.with_user(self.cashier).write({"inventory_quantity": 5})

    def test_cashier_cannot_create_partner(self):
        with self.assertRaises(AccessError):
            self.env["res.partner"].with_user(self.cashier).create({"name": "Nope"})

    def test_cashier_cannot_refund_line(self):
        with self.assertRaises(AccessError):
            self.env["pos.order.line"].with_user(self.cashier).create(
                {
                    "order_id": self.order.id,
                    "product_id": self.product.id,
                    "qty": -1,
                    "price_unit": 10.0,
                    "price_subtotal": -10.0,
                    "price_subtotal_incl": -10.0,
                }
            )

    def test_cashier_cannot_refund_backend(self):
        with self.assertRaises(AccessError):
            self.order.with_user(self.cashier)._refund()

    def test_cashier_cannot_escalate_to_manager(self):
        manager_group = self.env.ref("retail_management.group_retail_manager")
        with self.assertRaises(AccessError):
            self.cashier.with_user(self.cashier).write({"group_ids": [(4, manager_group.id)]})

    def _incoming_picking(self):
        return self.env["stock.picking"].create(
            {
                "picking_type_id": self.env.ref("stock.picking_type_in").id,
                "location_id": self.env.ref("stock.stock_location_suppliers").id,
                "location_dest_id": self.env.ref("stock.stock_location_stock").id,
                "move_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 5,
                            "product_uom": self.product.uom_id.id,
                            "location_id": self.env.ref("stock.stock_location_suppliers").id,
                            "location_dest_id": self.env.ref("stock.stock_location_stock").id,
                        },
                    )
                ],
            }
        )

    def test_cashier_cannot_validate_receipt(self):
        picking = self._incoming_picking()
        with self.assertRaises(AccessError):
            picking.with_user(self.cashier).button_validate()
        with self.assertRaises(AccessError):
            picking.with_user(self.cashier)._action_done()

    def test_manager_can_validate_receipt(self):
        picking = self._incoming_picking()
        picking.with_user(self.manager).action_confirm()
        picking.with_user(self.manager).move_ids.quantity = 5
        picking.with_user(self.manager).move_ids.picked = True
        picking.with_user(self.manager).button_validate()
        self.assertEqual(picking.state, "done")
        self.assertEqual(
            self.env["stock.quant"]._get_available_quantity(
                self.product, self.env.ref("stock.stock_location_stock")
            ),
            5,
        )

    # --- allowed operations ------------------------------------------------
    def test_cashier_can_read_products(self):
        self.assertTrue(self.product.with_user(self.cashier).read(["name"]))

    def test_cashier_can_create_normal_sale_line(self):
        line = self.env["pos.order.line"].with_user(self.cashier).create(
            {
                "order_id": self.order.id,
                "product_id": self.product.id,
                "qty": 1,
                "price_unit": 10.0,
                "price_subtotal": 10.0,
                "price_subtotal_incl": 10.0,
            }
        )
        self.assertEqual(line.qty, 1)

    def test_manager_can_create_refund_line(self):
        line = self.env["pos.order.line"].with_user(self.manager).create(
            {
                "order_id": self.order.id,
                "product_id": self.product.id,
                "qty": -1,
                "price_unit": 10.0,
                "price_subtotal": -10.0,
                "price_subtotal_incl": -10.0,
            }
        )
        self.assertEqual(line.qty, -1)

    def test_manager_can_create_product(self):
        product = self.env["product.product"].with_user(self.manager).create({"name": "Manager Product"})
        self.assertTrue(product.exists())

    def test_superuser_is_not_locked_out(self):
        # A guard must never block Odoo superusers, or the owner could not fix a bad setup.
        line = self.env["pos.order.line"].create(
            {
                "order_id": self.order.id,
                "product_id": self.product.id,
                "qty": -1,
                "price_unit": 10.0,
                "price_subtotal": -10.0,
                "price_subtotal_incl": -10.0,
            }
        )
        self.assertEqual(line.qty, -1)
        self.order._refund()
