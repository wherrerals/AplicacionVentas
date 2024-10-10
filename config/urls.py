from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('ventas/')),
    path('admin/', admin.site.urls),
    path('ventas/', include('showromVentasApp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('', include('logicaVentasApp.urls')),

]
