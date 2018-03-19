# Django core
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'lp/index.html'
