from unittest.mock import patch

from odoo.addons.base.models.ir_actions_report import IrActionsReport
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestInvoicePdfAttachment(TransactionCase):
    """D-033: posting a customer invoice stores its PDF, so the customer portal shows the invoice
    itself instead of a "proforma" preview."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "PDF Test Customer"})
        cls.invoice = cls.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": cls.partner.id,
                "invoice_line_ids": [(0, 0, {"name": "Item", "quantity": 1.0, "price_unit": 10.0})],
            }
        )

    def _skip_without_chart(self):
        if not self.env.company.chart_template:
            self.skipTest("no chart of accounts in this database, cannot post an invoice")

    def test_posting_attaches_pdf(self):
        self._skip_without_chart()
        with patch.object(
            IrActionsReport, "_render_qweb_pdf", return_value=(b"%PDF-1.4 test", "pdf")
        ):
            self.invoice.action_post()
        self.assertEqual(self.invoice.state, "posted")
        self.assertTrue(self.invoice.invoice_pdf_report_id)

    def test_pdf_failure_does_not_block_posting(self):
        self._skip_without_chart()
        with patch.object(IrActionsReport, "_render_qweb_pdf", side_effect=Exception("wkhtmltopdf")):
            self.invoice.action_post()
        self.assertEqual(self.invoice.state, "posted")
        self.assertFalse(self.invoice.invoice_pdf_report_id)

    def test_pdf_renders_in_customer_language(self):
        """D-035: the report follows the *session* language, so an invoice generated outside the web
        UI would reach an Arabic customer with English labels."""
        self._skip_without_chart()
        self.partner.lang = "ar_001"
        seen = {}

        def fake_render(records, report_ref, res_ids=None, data=None):
            seen["lang"] = records.env.lang   # the env the report was rendered with
            return b"%PDF-1.4 test", "pdf"

        with patch.object(IrActionsReport, "_render_qweb_pdf", autospec=True, side_effect=fake_render):
            self.invoice.action_post()
        self.assertEqual(seen.get("lang"), "ar_001")
