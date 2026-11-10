{
    "name": "Retail Management",
    "version": "19.0.1.9.0",
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
        "views/product_barcode_scan.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "retail_management/static/src/scss/apps_page.scss",
            "retail_management/static/src/apps_page/apps_page.js",
            "retail_management/static/src/xml/apps_page.xml",
            "retail_management/static/src/xml/apps_button.xml",
            # Product form: camera Scan button on the Barcode field (D-022)
            "retail_management/static/src/fields/barcode_scan_field.js",
            "retail_management/static/src/fields/barcode_scan_field.xml",
        ],
        # POS payment screen: two columns, full-size icons (D-019)
        # POS receipt: QR only, no portal URL or 5-char code (D-021)
        "point_of_sale._assets_pos": [
            "retail_management/static/src/pos/payment_methods.scss",
            "retail_management/static/src/pos/receipt.scss",
        ],
    },
    "application": True,
    "installable": True,
}
