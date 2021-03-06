from django import forms
from django.forms.models import modelform_factory
from django.urls import reverse

from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from dal import autocomplete

from .models import Court, Place


class CourtsList(ListView):
    model = Court
    paginate_by = 10

    def get_queryset(self, **kwargs):
        courts = Court.objects.all()
        if self.request.user.is_authenticated and self.request.user.city:
            courts = courts.filter(place__city=self.request.user.city)
        query = self.request.GET.get('q', None)
        if query:
            return courts.filter(title__icontains=query)
        return courts

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CourtsList, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


class CourtDetail(DetailView):
    model = Court
    context_object_name = 'court'

    def get_context_data(self, **kwargs):
        context = super(CourtDetail, self).get_context_data(**kwargs)
        
        # Increment court views
        context['court'].views += 1
        context['court'].save()
        return context


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
    fields = ['title', 'description', 'admin_description', 'place', 'type', 'price', 'photo']
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


class CourtAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Court.objects.none()
        all_courts = Court.objects.all()

        if self.q:
            # Search by Court.Place.address
            _addresses = all_courts.filter(place__address__icontains=self.q)
            # by Court.title
            _titles = all_courts.filter(title__icontains=self.q)

            return _titles | _addresses

        return all_courts

    def get_result_label(self, item):
        return u'{}, {}'.format(item.title, item.place.address)


class CourtUpdate(UpdateView):
    model = Court
    fields = '__all__'
    permission_required = 'courts.can_edit'
    template_name = 'courts/court_edit.html'
