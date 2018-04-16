# Django core
from django import forms
from django.forms.widgets import SelectDateWidget, ClearableFileInput
from django.contrib.auth import login, authenticate
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import (PasswordResetView, PasswordResetConfirmView)
from django.contrib.auth.forms import (AdminPasswordChangeForm, PasswordChangeForm)
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect

# Our apps
from .models import User

# Third party
from social_django.models import UserSocialAuth


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    error_messages = {
        'password_mismatch': "Пароли не совпадают.",
    }
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Повторите",
        widget=forms.PasswordInput,
        strip=False,
    )

    class Meta:
        model = User
        fields = ('email',)
        field_classes = {'email': forms.EmailField}

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


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
    paginate_by = 10

    def get_queryset(self, **kwargs):
        query = self.request.GET.get('q', None)
        users = User.objects.all()
        if self.request.user.is_authenticated and self.request.user.city:
            users = users.filter(city=self.request.user.city)
        if query:
            q1 = users.filter(first_name__contains=query)
            q2 = users.filter(last_name__contains=query)
            q3 = users.filter(phone__contains=query)
            return q1 | q2 | q3
        return users

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersList, self).get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


class UserDetail(DetailView):
    model = User
    context_object_name = 'object'


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'city', 'sex', 'bdate', 'phone', 'avatar']
        widgets = {
            'bdate': SelectDateWidget(years=list(range(1945, 2017))),
            'avatar': ClearableFileInput()
        }

    # def clean_bdate(self):
    #     bdate = self.cleaned_data.get("bdate")
    #     if bdate:
    #         if timezone.now().date() - bdate < timezone.timedelta(days=3650):
    #             raise forms.ValidationError("Тебе меньше 10 лет, серьезно?")
    #         return bdate
    #     else:
    #         return None


@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    model = User
    form_class = UserUpdateForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdate, self).get_context_data(**kwargs)

        try:
            vk_login = self.request.user.social_auth.get(provider='vk-oauth2')
        except UserSocialAuth.DoesNotExist:
            vk_login = None
        can_disconnect = (self.request.user.social_auth.count() > 1 or self.request.user.has_usable_password())

        context.update({'vk_login': vk_login, 'can_disconnect': can_disconnect})
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