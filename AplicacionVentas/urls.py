from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('showromVentasApp.urls')),
    path('', include('logicaVentasApp.urls')),
    path('accounts/', include('django.contrib.auth.urls'))
]
