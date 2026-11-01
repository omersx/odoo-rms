from odoo import _, api, models
from odoo.exceptions import AccessError

MANAGER_GROUP = "retail_management.group_retail_manager"


def is_retail_manager(env):
    """Managers and Odoo superusers pass; everyone else is subject to the retail restriction."""
    return env.is_admin() or env.user.has_group(MANAGER_GROUP)


class PosOrder(models.Model):
    _inherit = "pos.order"

    def _refund(self):
        """Refunds are a manager action (spec §3: cashier approves none by default)."""
        if not is_retail_manager(self.env):
            raise AccessError(_("Only a Retail Manager can create a refund."))
        return super()._refund()


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    # A negative quantity is how the POS records a refund. Guarding the line (rather than the
    # order) covers every path: POS sync, backend refund and direct RPC.
    @api.model_create_multi
    def create(self, vals_list):
        if any((vals.get("qty") or 0) < 0 for vals in vals_list) and not is_retail_manager(self.env):
            raise AccessError(_("Only a Retail Manager can make a refund (negative quantity)."))
        return super().create(vals_list)

    def write(self, vals):
        if (vals.get("qty") or 0) < 0 and not is_retail_manager(self.env):
            raise AccessError(_("Only a Retail Manager can make a refund (negative quantity)."))
        return super().write(vals)
