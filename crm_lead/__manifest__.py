{
    'name': "Customize CRM Lead",
    'author': "IDigiMeta",
    'version': '14.0',
    "category": 'CRM Lead',
    "summary": "Modify the menu, actions, and lead name. Create masters for regarding, category, and status. "
        "Add status bar and filter to lead form views. "
        "Set address fields to read-only and hide external info in the lead form.",
    "description":
        "Modify the menu, actions, and lead name. Create masters for regarding, category, and status. "
        "Add status bar and filter to lead form views. "
        "Set address fields to read-only and hide external info in the lead form.",
    'depends': ['base', 'crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'views/regarding_views.xml',
        'views/status_views.xml',
        'views/category_views.xml',
        'views/res_company_views.xml'

    ],
    'images': [
        'static/description/icon.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
