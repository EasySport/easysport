# Django core
from django.views.generic import ListView, DetailView

# Our apps
from .models import Court


class CourtsList(ListView):
    model = Court


class CourtDetail(DetailView):
    model = Court