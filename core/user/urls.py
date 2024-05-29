from django.urls import path
from core.user.views import *

app_name = 'user'

urlpatterns = [
    # User
    path('list/', UserListView.as_view(), name='userList'),
    path('add/', UserCreateView.as_view(), name='userCreate'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='userUpdate'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='userDelete'),
    path('change/group/<int:pk>/', UserChangeGroup.as_view(), name='userChangeGroup'),
    path('profile/', UserProfileView.as_view(), name='userProfile'),
    path('change/password/', UserChangePasswordView.as_view(), name='userChangePassword'),
]