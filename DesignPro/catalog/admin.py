from django.contrib import admin
from .models import CustomUser, DesignRequests, Category


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'patronym' )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'patronym')


admin.site.register(CustomUser, CustomUserAdmin)


class DesignRequestsAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description', 'created_at', 'status')
    search_fields = ('user', 'title', 'description', 'created_at', 'status')


admin.site.register(DesignRequests, DesignRequestsAdmin)
admin.site.register(Category)