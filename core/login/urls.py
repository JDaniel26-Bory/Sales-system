from django.urls import path
from core.login.views import *

urlpatterns = [
    path('', loginFormView.as_view(), name='login'),
    path('logout/', logoutView.as_view(), name='logout'),
    path('reset/password/', ResetPasswordView.as_view(), name='resetPassword'),
    path('change/password/<str:token>/', ChangePasswordView.as_view(), name='changePassword'),
    # path('logout/', logoutRedirectView.as_view(), name='logout'),
]
