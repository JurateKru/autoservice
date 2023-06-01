from django.contrib import admin
from . import models

# Register your models here.

class CarAdmin(admin.ModelAdmin):
    list_display = ('plate_nr', 'vin', 'client', 'car_model')
    list_filter = ('client', 'car_model')
    search_fields = ('plate_numer', 'vin')

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'engine', 'year')

class OrderEntryInline(admin.TabularInline):
    model = models.OrderEntry
    # readonly_fields = ('id', )
    # can_delete = False
    extra = 0

class OrderEntryAdmin(admin.ModelAdmin):
    list_display = ('quantity', 'price', 'service', 'order')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount')
    inlines = [OrderEntryInline]

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

admin.site.register(models.Car, CarAdmin)
admin.site.register(models.CarModel, CarModelAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Service, ServiceAdmin)
admin.site.register(models.OrderEntry, OrderEntryAdmin)

