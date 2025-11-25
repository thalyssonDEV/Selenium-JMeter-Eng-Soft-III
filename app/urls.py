from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/itens', views.api_itens, name='api_itens'),
    path('api/itens/<int:item_id>', views.api_item_detail, name='api_item_detail'),
]