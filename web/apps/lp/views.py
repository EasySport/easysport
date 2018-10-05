# Django core
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'lp/index.html'


class ContactsView(TemplateView):
    template_name = 'lp/contacts.html'


class DonateThanksView(TemplateView):
    template_name = 'lp/donate_thanks.html'
