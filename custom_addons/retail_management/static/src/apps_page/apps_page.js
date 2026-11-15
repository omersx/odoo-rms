import { Component, onMounted, useRef, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useBus, useService } from "@web/core/utils/hooks";
import { standardActionServiceProps } from "@web/webclient/actions/action_service";

/**
 * Full-screen app launcher, the page Odoo 16-18 showed when clicking the "apps" icon.
 * Odoo 19 replaced it with a text dropdown, so the owner asked for the old page back.
 * The menus (and the groups that filter them) still come from the menu service.
 */
export class AppsPage extends Component {
    static template = "retail_management.AppsPage";
    static props = { ...standardActionServiceProps };

    setup() {
        this.menu = useService("menu");
        this.state = useState({ search: "" });
        this.searchInput = useRef("search");
        // Menus are cached in the browser (menu service + localStorage); refresh on open and
        // re-render when they change, so a menu hidden server-side stops showing a tile here.
        useBus(this.env.bus, "MENUS:APP-CHANGED", () => this.render());
        onMounted(() => {
            this.searchInput.el?.focus();
            this.menu.reload();
        });
    }

    get apps() {
        const term = this.state.search.trim().toLowerCase();
        const apps = this.menu.getApps();
        return term ? apps.filter((app) => app.name.toLowerCase().includes(term)) : apps;
    }

    getHref(app) {
        return `/odoo/${app.actionPath || "action-" + app.actionID}`;
    }

    open(app) {
        this.menu.selectMenu(app);
    }
}

registry.category("actions").add("retail_management.apps_page", AppsPage);
