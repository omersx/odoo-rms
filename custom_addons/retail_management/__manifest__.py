{
    "name": "Retail Management",
    "version": "19.0.1.3.0",
    "summary": "Simplified retail workspace on top of native POS, Stock and Invoicing",
    "author": "RMS",
    "license": "LGPL-3",
    "category": "Sales/Point of Sale",
    "depends": ["point_of_sale", "stock", "account", "contacts"],
    "data": [
        "security/retail_security.xml",
        "data/hide_discuss.xml",
        "views/retail_menu.xml",
    ],
    "application": True,
    "installable": True,
}
