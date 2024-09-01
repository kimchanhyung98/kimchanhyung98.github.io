import os

AUTHOR = 'kimchanhyung98'
SITENAME = 'kimchanhyung98'
SITESUBTITLE = 'kimchanhyung blog'

if os.environ.get("CONTEXT") == "production":
    SITEURL = 'https://kimchanhyung98.github.io'
else:
    SITEURL = 'http://localhost:8000'

PATH = 'content'

# Regional Settings
TIMEZONE = 'Asia/Seoul'
DEFAULT_LANG = 'ko'
DATE_FORMATS = {'ko': '%Y-%m-%d'}

SITEMAP = {
    'format': 'xml',
    'priorities': {'articles': 0.5, 'indexes': 0.5, 'pages': 0.5},
    'changefreqs': {'articles': 'monthly', 'indexes': 'daily', 'pages': 'monthly'},
}

# Appearance
THEME = 'theme'
THEME_STATIC_DIR = 'theme'
TYPOGRIFY = True
DEFAULT_PAGINATION = 10

# Defaults
DEFAULT_CATEGORY = 'misc'
USE_FOLDER_AS_CATEGORY = False
ARTICLE_URL = '{slug}'
PAGE_URL = '{slug}'
PAGE_SAVE_AS = '{slug}.html'
TAGS_URL = 'tags'
CATEGORIES_URL = 'categories'
ARCHIVES_URL = 'archives'
SEARCH_URL = 'search'
# RELATIVE_URLS = True

# Feeds
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
CATEGORY_FEED_ATOM = None
CATEGORY_FEED_RSS = None
FEED_ALL_ATOM = None
TRANSLATION_FEED_ATOM = None

# Social
SOCIAL = (
    ('Contact', 'https://chanhyung.kim'),
    ('Github', 'https://github.com/kimchanhyung98', 'Github Profile'),
)

LINKS = (
    ('GitHub', 'https://github.com/kimchanhyung98'),
    # ('You can modify those links in your config file', '#'),
)

# Path
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
        'description': '구인구직, 커리어 계발',
    }
]

UTTERANCES_FILTER = True
COMMENTBOX_FILTER = True
