from odoo import _, models
from odoo.exceptions import AccessError

from .pos_order import is_retail_manager


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _check_stock_manager(self):
        """Receiving/adjusting stock is a manager action (spec §3).

        Only incoming/internal pickings are guarded: POS validates its own outgoing pickings as the
        cashier (`pos_order._create_order_picking` → `_action_done`), so blocking those would silently
        stop POS stock deduction.
        """
        if is_retail_manager(self.env):
            return
        if any(picking.picking_type_id.code in ("incoming", "internal") for picking in self):
            raise AccessError(_("Only a Retail Manager can receive or move stock."))

    def button_validate(self):
        self._check_stock_manager()
        return super().button_validate()

    def _action_done(self):
        self._check_stock_manager()
        return super()._action_done()
