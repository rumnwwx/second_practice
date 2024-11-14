from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    patronym = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password = models.CharField(max_length=100)
    password_confirm = models.CharField(max_length=100)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class DesignRequests(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    image_sale = models.FileField(blank=True, upload_to='images/', verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='', verbose_name='Категория')
    comments = models.TextField(blank=True, verbose_name='Комментарий')
    STATUS_CHOICES = [
        ('N', 'Новая'),
        ('P', 'Принято в работу'),
        ('C', 'Выполнено'),
    ]
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='N',
                              verbose_name='Статус')
    updated_image_sale = models.FileField(upload_to='admin_img/', verbose_name="Обновленное фото дизайна", blank=True, null=True)

    def __str__(self):
        return self.title


@receiver(pre_delete, sender=Category)
def delete_requests_with_category(sender, instance, **kwargs):
    DesignRequests.objects.filter(category=instance).delete()