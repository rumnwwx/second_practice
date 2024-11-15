from django.shortcuts import render
from django.views import generic
from .forms import CustomUserCreatingForm, CustomUserLoginForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.shortcuts import redirect
from .models import CustomUser


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
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        # Аутентификация пользователя
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Неправильное имя пользователя или пароль.')
            return self.form_invalid(form)


def custom_logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('index')
    else:
        return redirect('login')


class UserProfileListView(generic.ListView):
    model = CustomUser
    template_name = 'catalog/profile.html'


def user_agree(request):
    return render(request, 'catalog/user_agreement.html')
