from django.urls import path

from api_go.views.views import ProductsAPIView


urlpatterns = [

    path('products/', ProductsAPIView.as_view()),

]
