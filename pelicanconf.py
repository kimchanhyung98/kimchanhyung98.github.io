AUTHOR = 'kimchanhyung98'
SITENAME = 'kimchanhyung98.github.io'
SITEURL = ''

PATH = 'content'
# ARTICLE_PATHS = ['pages']

TIMEZONE = 'Asia/Seoul'

DEFAULT_LANG = 'ko'
DEFAULT_PAGINATION = 10

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

THEME = 'theme'
THEME_STATIC_DIR = 'theme'

# Blogroll
LINKS = (
    ('GitHub', 'https://github.com/kimchanhyung98'),
    # ('You can modify those links in your config file', '#'),
)

# Social widget
SOCIAL = (
    ('Contact', 'https://chanhyung.kim'),
    # ('You can add links in your config file', '#'),
)

STATIC_PATHS = [
    'images',
    'extra/CNAME',
    'extra/robots.txt',
]
EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/robots.txt': {'path': 'robots.txt'},
}

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
