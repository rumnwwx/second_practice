from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.shortcuts import render
from .models import CustomUser, DesignRequests
from django.contrib.auth import authenticate
from django.utils.safestring import mark_safe


class CustomUserCreatingForm(forms.ModelForm):
    username = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите имя пользователя'
        })
    )
    email = forms.CharField(
        label="",
        max_length=150,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Введите email'
        })
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите имя'
        })
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите фамилию'
        })
    )
    patronym = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите отчество'
        })
    )
    password = forms.CharField(label="", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="", widget=forms.PasswordInput)

    user_agreement = forms.BooleanField(
        label=mark_safe('Я согласен с <a href="/catalog/register/agreement/">условиями использования</a>'),
        required=True,
        widget=forms.CheckboxInput
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Такое имя пользователя занято.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Такой адрес электронной почты занят.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Пароли не совпадают")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ("username", "first_name", "last_name", 'patronym', 'email')


class CustomUserLoginForm(forms.Form):
    username = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите имя пользователя'
        })
    )
    password = forms.CharField(label="", widget=forms.PasswordInput)


class DesignRequestForm(forms.ModelForm):
    title = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Название заявки'
        })
    )

    description = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={
            'placeholder': 'Описание заявки',
            'rows': 4,
            'cols': 40
        })
    )

    image_sale = forms.FileField(
        label="",
        widget=forms.FileInput(),
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'bmp'])]
    )


    class Meta:
        model = DesignRequests
        fields = ['title', 'description', 'category', 'image_sale']

def your_view(request):
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                instance = DesignRequests()
                instance.title = form.cleaned_data['title']
                instance.description = form.cleaned_data['description']
                instance.image_sale = form.cleaned_data['image_sale']
                instance.save()
                return render(request, 'success.html')
            except ValueError:
                form.add_error(None, "Ошибка при сохранении данных.")
    else:
        form = DesignRequestForm()

    return render(request, 'design_request_list.html', {'form': form})

