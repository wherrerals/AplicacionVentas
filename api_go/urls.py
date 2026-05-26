from django.urls import path

from api_go.views.views import DocumentAPIView, DocumentDetailAPIView, ProductsAPIView, TechnicalSheetAPIView


urlpatterns = [

    path('products/', ProductsAPIView.as_view()),
    path('documents/', DocumentAPIView.as_view()),
    path('documents/details/', DocumentDetailAPIView.as_view()),
    path('technical-sheets/', TechnicalSheetAPIView.as_view())

]
