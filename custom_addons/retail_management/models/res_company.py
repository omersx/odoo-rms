from odoo import fields, models


class ResCompany(models.Model):
    """Wording of the invoice payment block (D-030), so a shop can change it without code."""

    _inherit = "res.company"

    rms_payment_title = fields.Char(
        string="Payment block title",
        default="طرق الدفع",
        help="Heading of the payment block printed on customer invoices.",
    )
    rms_payment_note = fields.Char(
        string="Payment note",
        default="ارسل اشعار الدفع في الرقم واتساب",
        help="Printed in front of the company phone number. Leave empty to print the number alone.",
    )
