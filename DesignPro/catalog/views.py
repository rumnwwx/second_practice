from django.shortcuts import render
from django.views import generic
from .forms import CustomUserCreatingForm, CustomUserLoginForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.shortcuts import redirect


def index(request):
    return render(request, 'index.html')


class Register(generic.CreateView):
    template_name = 'catalog/register.html'
    form_class = CustomUserCreatingForm
    success_url = reverse_lazy('login')


class Login(FormView):
    template_name = 'catalog/login.html'
    form_class = CustomUserLoginForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # Получаем данные из формы
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # Аутентификация пользователя
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            # Если аутентификация прошла успешно, логиним пользователя
            login(self.request, user)
            return super().form_valid(form)  # Перенаправление на success_url
        else:
            # Если аутентификация не удалась, добавляем ошибку
            form.add_error(None, 'Неправильное имя пользователя или пароль.')
            return self.form_invalid(form)  # Возвращаем форму с ошибкой


def custom_logout(request):
    if request.user.is_authenticated:
        auth_logout(request)  # Завершаем сессию пользователя
        return redirect('index')  # Перенаправляем на главную страницу или нужную страницу
    else:
        return redirect('login')