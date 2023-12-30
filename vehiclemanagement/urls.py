from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from . import settings

urlpatterns = [
    path('', include('website.urls')),
    path('django-admin/', admin.site.urls),
    path('admin/', include('adminsite.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('debug/', include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)