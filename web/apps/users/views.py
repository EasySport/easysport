from django import forms
from apps.users.models import User
from django.contrib.auth import login, authenticate
from django.views.generic.edit import FormView
from django.urls import reverse
from django.contrib.auth.views import (PasswordResetView, PasswordResetConfirmView)


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
        fields = ("email",)
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
        return reverse('games:list')

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

    def get_success_url(self):
        return reverse('users:password_reset_complete')

