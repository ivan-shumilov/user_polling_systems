from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)
    readonly_fields = ('register_token', 'password_reset_token', 'date_joined', 'last_login',)
    list_filter = ('is_superuser', 'is_staff', 'is_active')


admin.site.register(User, UserAdmin)
