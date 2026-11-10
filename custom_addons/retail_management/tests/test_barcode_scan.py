from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestBarcodeScanField(TransactionCase):
    def test_product_form_uses_barcode_scan_widget(self):
        """The Scan button lives on the widget, so the view arch must keep it (D-022)."""
        view = self.env.ref("product.product_template_only_form_view")
        arch = self.env["product.template"].get_view(view.id, "form")["arch"]
        self.assertIn('name="barcode"', arch)
        self.assertIn('widget="barcode_scan"', arch)
