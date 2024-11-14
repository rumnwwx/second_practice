from cProfile import label

from django.db import models
from django.contrib.auth.models import AbstractUser


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
    name=models.CharField(max_length=150)


    def __str__(self):
        return self.name


class DesignRequests(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image_sale = models.FileField(blank=True, upload_to='images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='')
    STATUS_CHOICES = [
        ('N', 'Новая'),
        ('P', 'Принято в работу'),
        ('C', 'Выполнено'),
    ]
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='new')

    def __str__(self):
        return self.title

