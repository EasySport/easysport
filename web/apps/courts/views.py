# Django core
from django import forms
from django.forms.models import modelform_factory
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse

# Our apps
from .models import Court, Place


class CourtsList(ListView):
    model = Court


class CourtDetail(DetailView):
    model = Court


class PlaceCreate(CreateView):
    model = Place
    fields = ['city', 'address']

    def get_success_url(self):
        return reverse('courts:create')


# Here's a mixin that allows you to define a widgets dictionary and still respects the fields list:
class ModelFormWidgetMixin(object):
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)


class CourtCreate(ModelFormWidgetMixin, CreateView):
    model = Court
    fields = '__all__'
    widgets = {
        'description': forms.Textarea(attrs={'rows': 3}),
        'admin_description': forms.Textarea(attrs={'rows': 3}),
    }

    def get_success_url(self):
        return reverse('courts:list')

    def get_initial(self):
        initial = super(CourtCreate, self).get_initial()
        initial = initial.copy()
        initial['place'] = Place.objects.latest('pk')
        return initial
