from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from main.views import IndexPageView, BackPageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('back/', BackPageView.as_view(), name='index'),
    path('', IndexPageView.as_view(), name='back'),

    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
