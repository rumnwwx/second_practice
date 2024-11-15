from django.contrib import admin
from .models import CustomUser, DesignRequests, Category
from django.core.exceptions import ValidationError
from django.db import transaction


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'patronym', 'confirmed',)
    search_fields = ('username', 'email', 'first_name', 'last_name', 'patronym', 'confirmed',)
    exclude = ['password_confirm']


admin.site.register(CustomUser, CustomUserAdmin)


class DesignRequestsAdmin(admin.ModelAdmin):
    readonly_fields = ('user', 'title', 'description', 'created_at','category')
    list_display = ('user', 'title', 'status', 'category', 'image_sale', 'comments')
    search_fields = ('user', 'title', 'description', 'created_at', 'status', 'category', 'comments')
    exclude = ['image_sale', 'category']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if obj:
            if obj.status == 'P':
                if 'updated_image_sale' in form.base_fields:
                    form.base_fields['updated_image_sale'].required = False
                    form.base_fields['updated_image_sale'].widget = admin.widgets.AdminFileWidget()

            elif obj.status == 'C':
                if 'comments' in form.base_fields:
                    form.base_fields['comments'].required = False
                    form.base_fields['comments'].widget = admin.widgets.AdminTextInputWidget()

        return form

    def save_model(self, request, obj, form, change):
        new_status = form.cleaned_data.get('status')
        image_sale = form.cleaned_data.get('updated_image_sale')
        comment = form.cleaned_data.get('comments')

        if new_status == 'C' and not image_sale:
            raise ValidationError("Для смены статуса на 'Выполнено' необходимо прикрепить изображение дизайна.")

        if new_status == 'P' and not comment:
            raise ValidationError("Для смены статуса на 'Принято в работу' необходимо добавить комментарий.")

        with transaction.atomic():
            obj.comment = comment or ''
            obj.done_status_image = image_sale
            super().save_model(request, obj, form, change)


admin.site.register(DesignRequests, DesignRequestsAdmin)

admin.site.register(Category)
