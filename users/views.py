import secrets
import random
import string

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    # чтобы обойти ошибку TemplateDoesNotExist at /users/register/
    template_name = 'users/register.html'
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        #  сохраняем пользователя
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class PasswordResetView(View):
    def get(self, request):
        return render(request, 'users/password_reset.html')

    def post(self, request):
        email = request.POST.get('email')
        user = get_object_or_404(User, email=email)

        # Генерация нового случайного пароля
        new_password = self.generate_random_password()

        # Хеширование нового пароля
        hashed_password = make_password(new_password)

        # Обновление пароля пользователя
        user.password = hashed_password
        user.save()

        # Отправка email с новым паролем
        send_mail(
            subject="Сброс пароля",
            message=f"Ваш новый пароль: {new_password}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return redirect('users:login')  # Перенаправление на страницу входа после отправки email

    def generate_random_password(self, length=8):
        """Генерация случайного пароля."""
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))