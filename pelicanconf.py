import os

# Defaults
if os.environ.get("CONTEXT") == "production":
    SITEURL = 'https://chanhyung.kim'
else:
    SITEURL = 'http://localhost:8000'

AUTHOR = 'kimchanhyung98'
SITENAME = 'Chandlery'
SITESUBTITLE = 'chanhyung.kim'

DEFAULT_CATEGORY = 'misc'
USE_FOLDER_AS_CATEGORY = False

# URL
PAGE_URL = '{slug}'
PAGE_SAVE_AS = '{slug}.html'

ARTICLE_URL = 'w/{slug}'
ARTICLE_SAVE_AS = 'w/{slug}.html'

ARCHIVES_URL = 'archives'
CATEGORIES_URL = 'categories'
SEARCH_URL = 'search'
TAGS_URL = 'tags'
# RELATIVE_URLS = True

# Path
PATH = 'content'
STATIC_PATHS = [
    'images',
    'extra/CNAME',
    'extra/robots.txt',
]

EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
    'extra/robots.txt': {'path': 'robots.txt'},
}

# Plugins
PLUGIN_PATHS = ['plugins']
PLUGINS = ['sitemap']
SITEMAP = {
    'format': 'xml',
    'priorities': {'articles': 0.5, 'indexes': 0.5, 'pages': 0.5},
    'changefreqs': {'articles': 'monthly', 'indexes': 'daily', 'pages': 'monthly'},
}

# Regional Settings
TIMEZONE = 'Asia/Seoul'
DEFAULT_LANG = 'ko'
DATE_FORMATS = {'ko': '%Y-%m-%d'}

# Appearance
THEME = 'theme'
THEME_STATIC_DIR = 'theme'
TYPOGRIFY = True
DEFAULT_PAGINATION = 10

# Feeds
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
CATEGORY_FEED_ATOM = None
CATEGORY_FEED_RSS = None
FEED_ALL_ATOM = None
TRANSLATION_FEED_ATOM = None

# Social
SOCIAL = (
    ('gitHub', 'https://github.com/kimchanhyung98'),
    ('linkedin', 'https://www.linkedin.com/in/kimchanhyung98'),
)

LINKS = (
    ('GitHub', 'https://github.com/kimchanhyung98'),
    # ('You can modify those links in your config file', '#'),
)

# Landing Page
# LANDING_PAGE_TITLE = 'Home'
PROJECTS_TITLE = '메모장'
PROJECTS = [
    {
        'name': 'GitHub',
        'url': 'https://github.com/kimchanhyung98',
        'description': '아무것도 모른다는 것을 안다',
    }, {
        'name': 'Linkedin',
        'url': 'https://www.linkedin.com/in/kimchanhyung98',
        'description': '구인구직',
    }
]

UTTERANCES_FILTER = True
COMMENTBOX_FILTER = True
