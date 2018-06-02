from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['email', 'password', 'last_login', 'phone']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'last_login',)}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email',
                                                'city', 'sex', 'bdate', 'phone',
                                                'avatar',)}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups',)}),
    )

admin.site.register(User, UserAdmin)
