from users.forms import SignUpForm, LoginForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import get_object_or_404
from .models import Profile


class RegistrationView(generic.CreateView):
    template_name = 'registration/register_form.html'
    form_class = SignUpForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:user_profile', args=(request.user,)))
        else:
            return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            return super(RegistrationView, self).form_valid(form)


class HomePageView(generic.TemplateView):
    template_name = 'registration/home_page.html'


class ProfileView(generic.DetailView):
    model = User
    template_name = "registration/profile_page.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "user"

    def get_object(self):
        user = get_object_or_404(Profile, user__username=self.kwargs['username'])
        if self.request.user.username == user.user.username:
            return user
        else:
            raise Http404


class LoginView(LoginRequiredMixin, RegistrationView):
    template_name = 'registration/login.html'
    model = Profile
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:user_profile', args=(request.user,)))
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if form.is_valid():
            return super(LoginView, self).form_valid(form)


