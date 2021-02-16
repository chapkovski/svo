from os import environ

SESSION_CONFIGS = [
    {
        'name': 'svoprimary',
        'display_name': 'SVO 6 items, 1 per page',
        'num_demo_participants': 1,
        'app_sequence': ['svo'],
        'random_order': True,

    },
    {
        'name': 'svofull',
        'display_name': 'SVO Measure. Full version (15 items), 1 per page',
        'num_demo_participants': 1,
        'app_sequence': ['svo'],
        'random_order': True,
        'secondary': True,
    },
    {
        'name': 'svoprimaryall',
        'display_name': 'SVO 6 items, all in one page',
        'num_demo_participants': 1,
        'app_sequence': ['svo'],
        'random_order': True,
        'items_per_page': 6,

    },
    {
        'name': 'svofullall',
        'display_name': 'SVO Measure. Full version (15 items), all in one page',
        'num_demo_participants': 1,
        'app_sequence': ['svo'],
        'random_order': True,
        'secondary': True,
        'items_per_page': 15,
    }
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'g&nvr6js_iyfx&%rpxy+ecj0(vp-i2-$#$uli6j5o09gy%be)y'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
