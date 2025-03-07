import os

# Defaults
if os.environ.get("CONTEXT") == "production":
    SITEURL = 'https://example.github.io'
else:
    SITEURL = 'http://localhost:8000'

AUTHOR = 'example_user'
SITENAME = 'Example'
SITESUBTITLE = 'example'

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
# - email, github, rss, facebook, twitter, linkedin, instagram, reddit, youtube, gmail, stackoverflow
# - hackernews, gitlab, calendar, wire, telegram, spotify, twitch, mastodon, keybase, goodreads
SOCIAL = (
    ('gitHub', 'https://github.com/example'),
    # ('You can modify those links in your config file', '#'),
)

LINKS = (
    ('GitHub', 'https://github.com/example'),
    # ('You can modify those links in your config file', '#'),
)

# Landing Page
# LANDING_PAGE_TITLE = 'Home'
PROJECTS_TITLE = '메모장'
PROJECTS = [
    {
        'name': 'GitHub',
        'url': 'https://github.com/example',
        'description': 'example_description',
    }, {
        'name': 'Linkedin',
        'url': 'https://www.linkedin.com/in/example',
        'description': 'example_description',
    }
]

UTTERANCES_FILTER = True
COMMENTBOX_FILTER = False
