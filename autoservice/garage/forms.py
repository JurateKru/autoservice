from django import forms
from . import models


class DateInput(forms.DateInput):
    input_type = 'date'


class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = models.OrderReview
        fields = ('content', 'order', 'reviewer')
        widgets = {
            'order': forms.HiddenInput(),
            'reviewer': forms.HiddenInput(),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ('due_back', 'car', 'status')
        widgets = {
            'due_back': DateInput(),
            'status': forms.HiddenInput(),
        }


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = models.Car
        fields =('car_model', 'plate_nr', 'vin', 'client', 'cover')
        widgets = {
            'client': forms.HiddenInput(),
        }
