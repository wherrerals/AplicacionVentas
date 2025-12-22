from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('ventas/')),
    path('admin/', admin.site.urls),
    path('ventas/', include('presentation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('upload/', include('uploadApp.urls')),
    path('api/v1/sgo/', include('api_go.urls')),

]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)