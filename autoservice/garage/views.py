from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from . models import Car, CarModel, Service, Order, OrderEntry
from django.views import generic

# Create your views here.

def index(request):
    service_count = Service.objects.all().count()
    count_orders = Order.objects.filter(status__exact=3).count()
    count_cars = Car.objects.all().count()

    context = {
        'service_count' : service_count,
        'count_orders' : count_orders,
        'count_cars' : count_cars,
    }

    return render(request, 'garage/index.html', context)

# visiems funkciniams views perduodam request
def car_model_list(request):
    return render(request, 'garage/car_models.html', {'car_model_list' : Car.objects.all()})

def car_detail(request, pk: int):
    return render(request, 'garage/car_detail.html', {'car' : get_object_or_404(Car, pk=pk)})

class OrderListView(generic.ListView):
    model = Order
    paginate_by = 5
    template_name = 'garage/order_list.html'

class OderDetailView(generic.DetailView):
    model = Order
    template_name = 'garage/order_detail.html'
