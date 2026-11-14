import base64
import logging

from odoo import models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        res = super().action_post()
        self._rms_attach_invoice_pdf()
        return res

    def _rms_attach_invoice_pdf(self):
        """Store the invoice PDF as the move's official file (D-033).

        The customer portal shows a *proforma* preview ("فاتورة شكلية") for any invoice that has no
        official PDF attached — including paid ones, which reads like a draft. Attaching the standard
        report here makes the portal print the real invoice. Posting must never fail because of it.
        """
        report = self.env.ref("account.account_invoices", raise_if_not_found=False)
        if not report:
            return
        to_attach = self.filtered(
            lambda move: move.move_type in ("out_invoice", "out_refund")
            and move.state == "posted"
            and not move.invoice_pdf_report_id
        )
        for move in to_attach:
            try:
                pdf, _report_type = (
                    self.env["ir.actions.report"]
                    .with_company(move.company_id)
                    ._render_qweb_pdf(report.report_name, move.ids)
                )
                move.invoice_pdf_report_file = base64.b64encode(pdf)
            except Exception:
                _logger.warning("could not attach the PDF of %s", move.name, exc_info=True)
