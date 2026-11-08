from odoo import fields, models


class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    # Core caps this at 50x50, which throws away most of a high-resolution icon. The tile still draws
    # it at 50 CSS px, so a larger source only shows on a high-DPI screen or when the page is zoomed.
    image = fields.Image("Image", max_width=256, max_height=256)
