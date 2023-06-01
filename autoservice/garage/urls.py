
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('car_models/', views.car_model_list, name='car_model_list'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', views.OderDetailView.as_view(), name='order_detail'),
]
