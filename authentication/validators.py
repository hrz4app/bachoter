from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def ForbiddenUsernamesValidator(value):
    forbidden_usernames = [
        'admin', 'settings', 'news',
        'about', 'help', 'signin',
        'signup', 'signout', 'terms', 
        'privacy', 'cookie', 'new', 
        'login', 'logout', 'administrator', 
        'join', 'account', 'username', 
        'root', 'blog', 'user',
        'users', 'billing', 'subscribe',
        'reviews', 'review', 'blog',
        'blogs', 'edit', 'mail',
        'email', 'home', 'job',
        'jobs', 'contribute', 'newsletter',
        'shop', 'profile', 'register',
        'auth', 'authentication', 'campaign',
        'config', 'delete', 'remove',
        'forum', 'forums', 'download',
        'downloads', 'contact', 'blogs',
        'feed', 'feeds', 'faq',
        'intranet', 'log', 'registration',
        'search', 'explore', 'rss',
        'support', 'status', 'static',
        'media', 'setting', 'css',
        'js', 'follow', 'activity',
        'questions', 'articles', 'network',
        'timeline', 'ajax', 'bachot',
        'message', 'messages', 'notifications',
        'buddy', 'buddies', 'accounts',
        'send', 'comment', 'acivate',
        'music', 'complete',
    ]
    if value.lower() in forbidden_usernames:
        raise ValidationError(u'This value is reserved and cannot be registered.')
    if len(value) < 4:
        raise ValidationError(u'Username must have at least 4 characters.')

def UniqueEmailEditValidator(email):
    def inner(value):
        if User.objects.filter(email__iexact=value).exclude(email__iexact=email).exists():
            raise ValidationError('User with this Email already exists.')
    return inner

DUPLICATE_EMAIL = _(u"This email address is already in use. "
                    u"Please supply a different email address.")
FREE_EMAIL = _(u"Registration using free email addresses is prohibited. "
               u"Please supply a different email address.")
RESERVED_NAME = _(u"This value is reserved and cannot be registered.")
TOS_REQUIRED = _(u"You must agree to the terms to register")

SPECIAL_HOSTNAMES = [
    'autoconfig',
    'autodiscover',
    'broadcasthost',
    'isatap',
    'localdomain',
    'localhost',
    'wpad',
]


PROTOCOL_HOSTNAMES = [
    'ftp',
    'imap',
    'mail',
    'news',
    'pop',
    'pop3',
    'smtp',
    'usenet',
    'uucp',
    'webmail',
    'www',
]


CA_ADDRESSES = [
    'admin',
    'administrator',
    'hostmaster',
    'info',
    'is',
    'it',
    'mis',
    'postmaster',
    'root',
    'ssladmin',
    'ssladministrator',
    'sslwebmaster',
    'sysadmin',
    'webmaster',
]


RFC_2142 = [
    'abuse',
    'marketing',
    'noc',
    'sales',
    'security',
    'support',
]


NOREPLY_ADDRESSES = [
    'mailer-daemon',
    'nobody',
    'noreply',
    'no-reply',
]


SENSITIVE_FILENAMES = [
    'clientaccesspolicy.xml',
    'crossdomain.xml',
    'favicon.ico',
    'humans.txt',
    'robots.txt',
    '.htaccess',
    '.htpasswd',
]


OTHER_SENSITIVE_NAMES = [
    'account',
    'accounts',
    'blog',
    'buy',
    'clients',
    'contact',
    'contactus',
    'contact-us',
    'copyright',
    'dashboard',
    'doc',
    'docs',
    'download',
    'downloads',
    'enquiry',
    'faq',
    'help',
    'inquiry',
    'license',
    'login',
    'logout',
    'payments',
    'plans',
    'portfolio',
    'preferences',
    'pricing',
    'privacy',
    'profile',
    'register'
    'secure',
    'signup',
    'ssl',
    'status',
    'subscribe',
    'terms',
    'tos',
    'user',
    'users'
    'weblog',
    'work',
]

DEFAULT_RESERVED_NAMES = (SPECIAL_HOSTNAMES + PROTOCOL_HOSTNAMES +
                          CA_ADDRESSES + RFC_2142 + NOREPLY_ADDRESSES +
                          SENSITIVE_FILENAMES + OTHER_SENSITIVE_NAMES)

class ReservedNameValidator(object):
    def __init__(self, reserved_names=DEFAULT_RESERVED_NAMES):
        self.reserved_names = reserved_names

    def __call__(self, value):
        if value in self.reserved_names or \
           value.startswith('.well-known'):
            raise ValidationError(
                RESERVED_NAME, code='invalid'
            )