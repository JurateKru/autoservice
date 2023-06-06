from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from . models import Car, CarModel, Service, Order, OrderEntry
from django.views import generic

# Create your views here.

def index(request):
    service_count = Service.objects.all().count()
    count_orders = Order.objects.filter(status__exact=3).count()
    count_cars = Car.objects.all().count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1 

    context = {
        'service_count' : service_count,
        'count_orders' : count_orders,
        'count_cars' : count_cars,
        'num_visits': num_visits,
    }

    return render(request, 'garage/index.html', context)

def car_model_list(request):
    qs = Car.objects
    query = request.GET.get('query')
    if query:
        qs = qs.filter(
            Q(car_model__make__icontains=query) |
            Q(car_model__model__icontains=query)
        )
    else:
        qs = qs.all()
    paginator = Paginator(qs, 5)
    car_model_list = paginator.get_page(request.GET.get('page'))
    return render(request, 'garage/car_models.html', {'car_model_list' : car_model_list})

def car_detail(request, pk: int):
    return render(request, 'garage/car_detail.html', {'car' : get_object_or_404(Car, pk=pk)})

class OrderListView(generic.ListView):
    model = Order
    paginate_by = 5
    template_name = 'garage/order_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            qs  =qs.filter(
                Q(car__plate_nr__icontains=query) |
                Q(car__vin__icontains=query) |
                Q(car__client__icontains=query) |
                Q(car__car_model__make__icontains=query) |
                Q(car__car_model__model__icontains=query)
            )
        return qs

class OderDetailView(generic.DetailView):
    model = Order
    template_name = 'garage/order_detail.html'


class UserOrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'garage/user_orders_list.html'
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(car__client=self.request.user)
        return qs
