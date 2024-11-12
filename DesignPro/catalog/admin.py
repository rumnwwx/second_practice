from django.contrib import admin
from .models import CustomUser, DesignRequests


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'patronym' )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'patronym')


admin.site.register(CustomUser, CustomUserAdmin)


class DesignRequestsAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description', 'created_at')
    search_fields = ('user', 'title', 'description', 'created_at')


admin.site.register(DesignRequests, DesignRequestsAdmin)