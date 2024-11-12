from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'patronym' )  # Укажите поля для отображения в списке
    search_fields = ('username', 'email', 'first_name', 'last_name', 'patronym')  # Поля для поиска


admin.site.register(CustomUser, CustomUserAdmin)

