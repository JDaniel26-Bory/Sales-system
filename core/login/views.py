from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.shortcuts import redirect, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView
import config.settings as setting
from core.login.forms import ResetPasswordForm, ChangePasswordForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from config import settings
from core.user.models import User
from config.wsgi import *
from django.template.loader import render_to_string
import uuid
from django.contrib.auth.models import User  # Suponiendo que usas el modelo User para autenticación
from django.core.mail import EmailMessage

class loginFormView(LoginView):
    template_name = 'login/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
           return redirect(setting.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Iniciar Sesion'
        return context
    
class loginFormView2(FormView):
    form_class = AuthenticationForm
    template_name = 'login/login.html'
    success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('erp:categoryList')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Iniciar Sesion'
        return context

class logoutView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)
    
class ResetPasswordView(FormView):
    form_class = ResetPasswordForm
    template_name = 'login/reset_password.html'
    success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def send_email_reset_pwd(self, user):
        data = {}
        try:
            user.token = uuid.uuid4()
            user.save()

            URL = settings.DOMAIN if not settings.DEBUG else self.request.META['HTTP_HOST']
            link_resetpwd = 'http://{}/login/change/password/{}/'.format(URL, str(user.token))
            link_home = 'http://{}'.format(URL)

            content = render_to_string('login/send_email.html', {
                'user': user,
                'link_resetpwd': link_resetpwd,
                'link_home': link_home
            })

            email = EmailMessage(
                subject='Cambio de contraseña',
                body=content,
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email],
            )
            email.content_subtype = 'html'  # Establecer el tipo de contenido a HTML

            # Conexión segura con TLS
            email.connection.start_tls(certfile=None, keyfile=None)  # Ajusta para certificados personalizados si es necesario
            email.send()

        except Exception as e:
            data['error'] = str(e)
        return data


    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                user = form.get_user()
                data = self.send_email_reset_pwd(user)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Cambio de Contraseña'
        return context

class ChangePasswordView(FormView):
    form_class = ChangePasswordForm
    template_name = 'login/changepwd.html'
    success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        token = self.kwargs['token']
        if User.objects.filter(token=token).exists():
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect('/')

    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                user = User.objects.get(token=self.kwargs['token'])
                user.set_password(request.POST['password'])
                user.token = uuid.uuid4()
                user.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['title'] = 'Cambio de Contraseña'
        context['login_url'] = settings.LOGIN_URL
        return context