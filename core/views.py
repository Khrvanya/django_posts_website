from django.shortcuts import render, redirect
from django.urls import reverse

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password

from django.views.generic.edit import FormView
from .forms import LoginForm, RegisterForm
from .models import User


class RegisterView(FormView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        content = {}
        content['form'] = RegisterForm
        return render(request, 'register.html', content)

    def post(self, request):
        content = {}
        form = RegisterForm(request.POST, request.FILES or None)
        if form.is_valid():
            save_it = form.save(commit=False)
            save_it.password = make_password(form.cleaned_data['password'])
            save_it.save()
            login(request, save_it)
            return redirect(reverse('posts:posts-view'))
        content['form'] = form
        template = 'register.html'
        return render(request, template, content)


class LoginView(FormView):

    content = {}
    content['form'] = LoginForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        content = {}
        if request.user.is_authenticated:
            return redirect(reverse('posts:posts-view'))
        content['form'] = LoginForm
        return render(request, 'login.html', content)

    def post(self, request):
        content = {}
        username = request.POST['username']
        password = request.POST['password']
        try:
            users = User.objects.filter(username=username)
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect(reverse('posts:posts-view'))
        except Exception as e:
            content = {}
            content['form'] = LoginForm
            content['error'] = 'Unable to login with provided credentials' # + str(e)
            return render(request, 'login.html', content)


class LogoutView(FormView):

    def get(self, request):
        logout(request)
        return redirect(reverse('core:base-view'))
        
        
class BaseView(FormView):

    def get(self, request):
        return render(request, 'base.html', {})
    