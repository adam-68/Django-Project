from .forms import SignUpForm, LoginForm
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import login, authenticate
from django.views import generic

from django.shortcuts import get_object_or_404
from .models import Profile, CustomUser


class RegistrationView(generic.FormView):
    template_name = 'registration/register_form.html'
    form_class = SignUpForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:user_profile', args=(request.user.profile.username,)))
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        user.refresh_from_db()
        request = self.request
        user.profile.username = form.cleaned_data['username']
        user.profile.first_name = form.cleaned_data['first_name']
        user.profile.last_name = form.cleaned_data['last_name']
        user.profile.birth_date = form.cleaned_data['birth_date']
        user.profile.email = form.cleaned_data['email']
        user.save()

        user = authenticate(request, email=user.email, password=form.cleaned_data['password1'])
        login(request, user)
        messages.success(request, ('You are successfully signed up!',))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:user_profile', args=(self.request.user.profile.username,))


class HomePageView(generic.TemplateView):
    template_name = 'registration/home_page.html'


class ProfileView(generic.DetailView):
    model = CustomUser
    template_name = "registration/profile_page.html"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_object(self):
        user = get_object_or_404(Profile, user__username=self.kwargs['username'])
        if user:
            return user
        else:
            raise Http404('User does not exist.')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, "User you are looking for does not exist.")
            return render(request, "registration/profile_page.html", {"user": request.user, "profile": request.user.profile})
        else:
            return HttpResponseRedirect(reverse("users:login"))


class UserLoginView(generic.FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:user_profile', args=(request.user.profile.username,)))
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.clean()
        if user:
            user = authenticate(self.request, email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            login(self.request, user)
            messages.success(self.request, ('You are successfully signed up!',))
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:user_profile', args=(self.request.user.profile.username,))




