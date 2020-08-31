from django.contrib import admin
from django.urls import path
from .views import LoginView, RegisterView, LogoutView, BaseView

app_name = 'core'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login-view'),
    path('register/', RegisterView.as_view(), name='register-view'),
    path('logout/', LogoutView.as_view(), name='logout-view'),
    path('', BaseView.as_view(), name='base-view'), 
]
