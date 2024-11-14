from django.shortcuts import render
from django.views import generic
from .forms import CustomUserCreatingForm, CustomUserLoginForm, DesignRequestForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.shortcuts import redirect
from .models import CustomUser, DesignRequests
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView


def index(request):
    design_requests = DesignRequests.objects.order_by('-created_at')[:4]

    context = {
        'design_requests': design_requests,
    }

    return render(request,'catalog/design_all_list.html',context)


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


class UserProfileListView(LoginRequiredMixin, generic.ListView):
    model = CustomUser
    template_name = 'catalog/profile.html'


def user_agree(request):
    return render(request, 'catalog/user_agreement.html')


class DesignRequestCreateView(LoginRequiredMixin, generic.CreateView):
    model = DesignRequests
    form_class = DesignRequestForm
    template_name = 'catalog/design_request_create.html'
    success_url = '/catalog/profile/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DesignRequestListView(LoginRequiredMixin, generic.ListView):
    model = DesignRequests
    template_name = 'catalog/design_request_list.html'
    context_object_name = 'design_requests'
    success_url = '/catalog/profile/'

    def get_queryset(self):
        return DesignRequests.objects.filter(user=self.request.user)


class DesignRequestDelete(DeleteView):
    model = DesignRequests
    success_url = reverse_lazy('design_request_view')
    template_name = 'catalog/design_request_delete.html'

    def get_queryset(self):
        return super().get_queryset()
