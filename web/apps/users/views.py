import requests

# Django core
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (AdminPasswordChangeForm,
                                       PasswordChangeForm)
from django.contrib.auth.views import (PasswordResetConfirmView,
                                       PasswordResetView)
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db.models import Q
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormView, UpdateView

# Third party
from social_django.models import UserSocialAuth

from .forms import UserCreationForm, UserUpdateForm
# Our apps
from .models import User
from apps.courts.models import City


class RegistrationView(FormView):
    template_name = 'registration/reg.html'
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse('users:update')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=raw_password)
        login(self.request, user)
        return super().form_valid(form)


class ResetView(PasswordResetView):
    template_name = 'registration/password/password_reset_form.html'
    email_template_name = 'registration/password/password_reset_email.html'

    def get_success_url(self):
        return reverse('users:password_reset_done')


class ResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password/password_reset_confirm.html'
    post_reset_login = True
    post_reset_login_backend = 'django.contrib.auth.backends.ModelBackend'

    def get_success_url(self):
        return reverse('users:update')


class UsersList(ListView):
    model = User
    paginate_by = 20
    context_object_name = 'users_list'

    def get_queryset(self, **kwargs):
        query = self.request.GET.get('q', '')
        users = User.objects.all().order_by('-last_login')

        if self.request.user.is_authenticated and self.request.user.city:
            users = users.filter(city=self.request.user.city)

        if query:
            q1 = users.filter(first_name__icontains=query)
            q2 = users.filter(last_name__icontains=query)
            q3 = users.filter(Q(phone__contains=query) & Q(phone_privacy=False))
            return q1 | q2 | q3
        return users

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersList, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


class UserDetail(DetailView):
    model = User
    context_object_name = 'current_user'


@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    model = User
    context_object_name = 'current_user'
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        user = self.request.user
        new_user = self.request.GET.get('new_user', None)
        # May be first social auth
        if new_user:
            vk_login = user.get_vk_login()
            if vk_login:
                # avatar preload
                avatar_url = vk_login.extra_data['photo_200_orig']
                if avatar_url:
                    r = requests.get(avatar_url)
                    if r.status_code == requests.codes.ok:
                        img_temp = NamedTemporaryFile(delete=True)
                        img_temp.write(r.content)
                        img_temp.flush()

                        user.avatar.save('avatar', File(img_temp), save=True)

                user.sex = 'm' if vk_login.extra_data['sex'] == 2 else 'f'
                user.bdate = vk_login.extra_data['bdate']
                try:
                    city_str = vk_login.extra_data['city']['title']
                    if city_str:
                        city = City.objects.get(title=vk_login.extra_data['city']['title'])
                        user.city = city
                except City.DoesNotExist:
                    pass

            fb_login = user.get_fb_login()
            if fb_login:
                pass
                # TODO: add facebook data to user
                # user.first_name = 'Facebook'
        return user

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdate, self).get_context_data(**kwargs)

        can_disconnect = (self.request.user.social_auth.count() > 1 or self.request.user.has_usable_password())

        context.update({
            'vk_login': self.request.user.get_vk_login(),
            'fb_login': self.request.user.get_fb_login(),
            'can_disconnect': can_disconnect}
        )
        return context


@login_required
def password(request):
    if request.user.has_usable_password():
        password_form = PasswordChangeForm
    else:
        password_form = AdminPasswordChangeForm

    if request.method == 'POST':
        form = password_form(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users:update')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = password_form(request.user)
    return render(request, 'users/password.html', {'form': form})


class ObtainView(TemplateView):
    template_name = 'users/obtain_rights.html'
