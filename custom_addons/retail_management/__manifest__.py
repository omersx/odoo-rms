{
    "name": "Retail Management",
    "version": "19.0.1.6.0",
    "summary": "Simplified retail workspace on top of native POS, Stock and Invoicing",
    "author": "RMS",
    "license": "LGPL-3",
    "category": "Sales/Point of Sale",
    "depends": ["point_of_sale", "stock", "account", "contacts"],
    "data": [
        "security/retail_security.xml",
        "data/hide_apps.xml",
        "views/retail_menu.xml",
        "views/apps_page_action.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "retail_management/static/src/scss/apps_page.scss",
            "retail_management/static/src/apps_page/apps_page.js",
            "retail_management/static/src/xml/apps_page.xml",
            "retail_management/static/src/xml/apps_button.xml",
        ],
    },
    "application": True,
    "installable": True,
}
