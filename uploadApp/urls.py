# urls.py de tu app
from django.urls import path
from . import views

urlpatterns = [
    path('subir/', views.subir_imagen, name='subir_imagen'),
    path('imagenes/', views.ver_imagenes, name='ver_imagenes'),
    path('subir-multiples/', views.subir_multiples_imagenes, name='subir_multiples'),

]
