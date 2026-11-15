import { AttachmentView } from "@mail/core/common/attachment_view";
import { onMounted, onWillUnmount } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";

// Odoo 19 has no control that hides the invoice preview pane (mail's pill only moves
// it to another window), so this adds a tab on the right edge of the screen that
// collapses and expands the pane.
// shortcut: the pane is hidden with CSS only; take over core's control if it ships one.
const COLLAPSED = "o_rms_preview_collapsed";
let toggleEl = null;

patch(AttachmentView.prototype, {
    setup() {
        super.setup();
        onMounted(() => this._rmsMountPaneToggle());
        onWillUnmount(() => this._rmsUnmountPaneToggle());
    },

    _rmsMountPaneToggle() {
        const pane = document.querySelector(".o_attachment_preview");
        if (!pane || toggleEl) {
            return; // no pane (e.g. portal chatter), or the tab is already mounted
        }
        const button = document.createElement("button");
        button.type = "button";
        button.className = "o_rms_pane_toggle btn btn-dark btn-sm";
        button.textContent = "»";
        button.title = "إخفاء المعاينة";
        // Inline, because Odoo's RTL stylesheet swaps left/right in our SCSS.
        button.style.top = "45%";
        button.style.right = "0";
        button.addEventListener("click", () => {
            const collapsed = pane.classList.toggle(COLLAPSED);
            button.textContent = collapsed ? "«" : "»";
            button.title = collapsed ? "إظهار المعاينة" : "إخفاء المعاينة";
        });
        document.body.append(button);
        toggleEl = button;
    },

    _rmsUnmountPaneToggle() {
        toggleEl?.remove();
        toggleEl = null;
    },
});
