from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('ventas/')),
    path('admin/', admin.site.urls),
    path('ventas/', include('showromVentasApp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('', include('logicaVentasApp.urls')),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
