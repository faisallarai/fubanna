from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from main.views import home_files

urlpatterns = [
    re_path(r'^(?P<filename>(robots.txt)|(humans.txt))$',
            home_files, name='home-files'),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('admin/statuscheck/', include('celerybeat_status.urls')),
    path('', include('main.urls', namespace='main')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
)

if settings.DEBUG:
    urlpatterns = urlpatterns + \
        static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
