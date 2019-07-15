"""bachoter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

from authentication.views_hmac import RegistrationView
from authentication.decorators import logout_required

from core import views as core_views
from social import views as social_views
from messenger import views as messenger_views
from notifications import views as notifications_views
from search import views as search_views
from entertainment import views as entertainment_views
 
urlpatterns = [
	url(r'^$', core_views.landing, name='landing'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^timeline/$', social_views.timeline, name='timeline'),

    url(r'^register/$', logout_required(RegistrationView.as_view()), name='registration_register'),
    url(r'^login/$', logout_required(auth_views.login), name='auth_login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login/'}, name='auth_logout'),
    url(r'^', include('registration.backends.hmac.urls')),

    url(r'^settings/$', core_views.settings_profile, name='settings_profile'),
    url(r'^settings/accounts/$', core_views.settings_accounts, name='settings_accounts'),
    url(r'^settings/password/$', auth_views.password_change, {'post_change_redirect': reverse_lazy('auth_password_change_done')}, name='auth_password_change'),

    url(r'^buddy/buddy-click/$', social_views.buddy_click, name='buddy_click'),

    url(r'^buddies/$', social_views.buddies, name='buddies'),
    url(r'^buddies/request/$', social_views.buddies_request, name='buddies_request'),
    url(r'^buddies/pending/$', social_views.buddies_pending, name='buddies_pending'),

    url(r'^bachot/(\d+)/$', social_views.bachot, name='bachot'),
    url(r'^bachot/create/$', social_views.bachot_create, name='bachot_create'),
    url(r'^bachot/bachot-form/$', social_views.bachot_form, name='bachot_form'),
    url(r'^bachot/like/$', social_views.bachot_like_or_dislike, name='bachot_like_or_dislike'),
    url(r'^bachot/delete/$', social_views.bachot_delete, name='bachot_delete'),
    url(r'^bachot/comment/$', social_views.bachot_comment, name='bachot_comment'),
    url(r'^bachot/get-comments/$', social_views.get_bachot_comments, name='get_bachot_comments'),
    url(r'^bachot/delete-comment/$', social_views.bachot_comment_delete, name='bachot_comment_delete'),

    url(r'^messages/$', messenger_views.default_messages, name='default_messages'),
    url(r'^messages/new/$', messenger_views.new_messages, name='new_messages'),
    url(r'^messages/send/$', messenger_views.send_messages, name='send_messages'),
    url(r'^messages/(?P<username>[^/]+)/$', messenger_views.with_messages, name='with_messages'),

    url(r'^search/$', search_views.search, name='search'),

    url(r'^notifications/$', notifications_views.notifications, name='notifications'),

    url(r'^music/(\d+)/$', entertainment_views.music_track, name='music_track'),

    url(r'^(?P<username>[^/]+)/buddies/$', core_views.profile_buddies, name='profile_buddies'),
    url(r'^(?P<username>[^/]+)/$', core_views.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)