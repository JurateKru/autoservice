
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('car_models/', views.car_model_list, name='car_model_list'),
    path('car/<int:pk>/', views.car_detail, name='car_detail'),
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', views.OderDetailView.as_view(), name='order_detail'),
    path('orders/my/', views.UserOrderListView.as_view(), name='user_orders'),
    path('order/create', views.OrderCreateView.as_view(), name='order_create'),
    path('cars/my', views.UserCarListView.as_view(), name='user_car_list')
]
