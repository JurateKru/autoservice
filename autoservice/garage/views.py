from typing import Any, Dict, Optional, Type
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.core.paginator import Paginator
from datetime import date, timedelta
from django.db.models.query import QuerySet
from django.db.models import Q
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from . forms import OrderReviewForm, OrderForm, CarCreateForm
from . models import Car, CarModel, Service, Order, OrderEntry


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
            qs = qs.filter(
                 Q(car__plate_nr__icontains=query) |
                Q(car__vin__icontains=query) |
                Q(car__client__first_name__icontains=query) |
                Q(car__client__last_name__icontains=query) |
                Q(car__car_model__make__icontains=query) |
                Q(car__car_model__model__icontains=query)
            )
        return qs



class OderDetailView(generic.edit.FormMixin, generic.DetailView):
    model = Order
    template_name = 'garage/order_detail.html'
    form_class = OrderReviewForm
    
    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['order'] = self.get_object()
        initial['reviewer'] = self.request.user
        return initial 

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_valid(self, form: Any) -> HttpResponse:
        form.instance.order = self.get_object()
        form.instance.reviewer = self.request.user
        form.save()
        messages.success(self.request, _('Comment posted!'))
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse('order_detail', kwargs={'pk':self.get_object().pk})


class UserOrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = 'garage/user_orders_list.html'
    paginate_by = 7

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(car__client=self.request.user)
        return qs
    
class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'garage/order_form.html'

    def get_form(self, form_class: Type[BaseModelForm] | None = form_class) -> BaseModelForm:
        form = super().get_form(form_class)
        if not form.is_bound:
            form.fields["car"].queryset = Car.objects.filter(client=self.request.user)
        return form

    def get_success_url(self) -> str:
        return reverse('user_orders')
    
    def form_valid(self, form):
        form.instance.order = self.request.user
        return super().form_valid(form)
    
    def get_absolute_url(self):
        return reverse('order_detail', args=[str(self.id)])
    
    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        car_id = self.request.GET.get('car_id')
        if car_id:
            initial['car'] = get_object_or_404(Car, id=car_id)
        initial['status'] = 0
        initial['due_back'] = date.today() + timedelta(days=14)
        return initial


class UserCarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    template_name = 'garage/user_car_list.html'
    context_object_name = 'car_list'

    def get_queryset(self):
        return Car.objects.filter(client=self.request.user)


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarCreateForm
    template_name = 'garage/user_car_create.html'

    def get_initial(self) -> Dict[str, Any]:
        initial =  super().get_initial()
        initial['client'] = self.request.user
        return initial
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.client = self.request.user
        messages.success(self.request, 'Car is created successfully')
        return super().form_valid(form)


class CarUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Car
    form_class = CarCreateForm
    template_name = 'garage/user_car_update.html'
    # success_url = reverse_lazy('user_car_list')

    def get_initial(self) -> Dict[str, Any]:
        initial =  super().get_initial()
        initial['client'] = self.request.user
        return initial
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.client = self.request.user
        messages.success(self.request, 'Car is updated successfully')
        return super().form_valid(form)
    
    def test_func(self) -> bool | None:
        obj = self.get_object()
        return obj.client == self.request.user
    
    def get_success_url(self) -> str:
        return reverse('car_detail', kwargs={'pk':self.get_object().pk})


class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Order
    template_name = 'garage/order_delete.html'
    success_url = reverse_lazy('user_orders')

    def form_valid(self, form):
        messages.success(self.request, 'Order is deleted successfully')
        return super().form_valid(form)

    def test_func(self) -> bool | None:
        obj = self.get_object()
        return obj.client == self.request.user
