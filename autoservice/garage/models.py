from django.contrib.auth import get_user_model
from datetime import date
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from tinymce.models import HTMLField


User = get_user_model()

# Create your models here.

class CarModel(models.Model):
    make =models.CharField(_("make"), max_length=50)
    model = models.CharField(_("model"), max_length=50)
    engine = models.CharField(_("engine"), max_length=50, null=True, blank=True)
    year = models.IntegerField(_("year"), null=True, blank=True)

    class Meta:
        verbose_name = _("car model")
        verbose_name_plural = _("car models")

    def __str__(self):
        return f'{self.make} {self.model}'

    def get_absolute_url(self):
        return reverse("carmodel_detail", kwargs={"pk": self.pk})
    

class Car(models.Model):
    plate_nr = models.CharField(_("plate number"), max_length=50)
    vin = models.CharField(_("VIN"), max_length=50)
    notes = HTMLField(_("notes"), max_length=8000, blank=True, null=True)
    car_model = models.ForeignKey(
        CarModel,
        verbose_name=_("car model"),
        on_delete=models.SET_NULL,
        null=True,
        related_name='cars') 
    
    client = models.ForeignKey(
        User, 
        verbose_name=_("client"), 
        on_delete=models.CASCADE,
        related_name='cars',
        null=True,
        blank=True)
    

    class Meta:
        verbose_name = _("car")
        verbose_name_plural = _("cars")

    def __str__(self):
        return self.plate_nr

    def get_absolute_url(self):
        return reverse("car_detail", kwargs={"pk": self.pk})
    
    cover = models.ImageField(
        _("cover"),
        upload_to='garage/car_covers',
        null=True,
        blank=True,
    )
    
class Order(models.Model):
    date = models.DateField(_("date"), auto_now=False, auto_now_add=True)
    # amount = models.DecimalField(_("amount"), max_digits=18, decimal_places=2)
    car = models.ForeignKey(
        Car,
        verbose_name=_("car"), 
        on_delete=models.CASCADE,
        related_name='orders') 
    due_back = models.DateField(_("due back"), null=True, blank=True, db_index=True)

    @property
    def client(self):
        return self.car.client
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False  
    
    @property
    def amount(self):
        order_entries = OrderEntry.objects.filter(order=self.id)
        price = 0
        for order_entry in order_entries:
            price += order_entry.price
        return price

    class Meta:
        ordering = ['date', 'id']
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return f'{self.date} {self.car}'

    def get_absolute_url(self):
        return reverse("order_detail", kwargs={"pk": self.pk})
    
    STATUS_CHOICES = (
        (0, _('In a Row')),
        (1, _('Working')),
        (2, _('Pending')),
        (3, _('Done')),
        (7, _('Cancelled')),
    )

    status = models.PositiveSmallIntegerField(
        _("status"), 
        choices=STATUS_CHOICES, 
        default=0,
        db_index=True
    )


class Service(models.Model):
    name = models.CharField(_("name"), max_length=100)
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2)
    class Meta:
        verbose_name = _("service")
        verbose_name_plural = _("services")

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("service_detail", kwargs={"pk": self.pk})

class OrderEntry(models.Model):
    quantity = models.IntegerField(_("quantity"))
    # price = models.DecimalField(_("price"), max_digits=18, decimal_places=2)
    service = models.ForeignKey(
        Service,
        verbose_name=_("service"),
        on_delete=models.CASCADE,
        related_name='entries')
    order = models.ForeignKey(
        Order, 
        verbose_name=_("order"),
        on_delete=models.CASCADE,
        related_name='entries')
    
    @property
    def price(self):
        return self.quantity * self.service.price

    class Meta:
        verbose_name = _("order entry")
        verbose_name_plural = _("order entries")

    def __str__(self):
        return f"{self.order}. {self.service}, {self.quantity}, {self.price}"

    def get_absolute_url(self):
        return reverse("orderentry_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if self.price == 0:
            self.price = self.service.price
        super().save(*args, **kwargs)

class OrderReview(models.Model):
    order = models.ForeignKey(
        Order, 
        verbose_name=_("order"), 
        on_delete=models.CASCADE,
        related_name='reviews')
    reviewer = models.ForeignKey(
        User, 
        verbose_name=_("reviewer"), 
        on_delete=models.SET_NULL,
        related_name='order_reviews',
        null=True, blank=True,
        )
    reviewed_at = models.DateTimeField(_("Reviewed"), auto_now_add=True)
    content = models.TextField(_("content"), max_length=4000)
    
    class Meta:
        ordering = ['-reviewed_at']
        verbose_name = _("order review")
        verbose_name_plural = _("order reviews")

    def __str__(self):
        return f"{self.reviewed_at}: {self.reviewer}"

    def get_absolute_url(self):
        return reverse("orderReview_detail", kwargs={"pk": self.pk})
