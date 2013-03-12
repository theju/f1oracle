from .forms import RegisterForm, LoginForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, \
    login as django_login, logout as django_logout

def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data["username"],
                                            email=data.get("email", ""),
                                            password=data["password1"])
            auth_user = authenticate(username=data["username"],
                                     password=data["password1"])
            django_login(request, auth_user)
            return HttpResponseRedirect(reverse("dashboard"))
    return render_to_response("accounts/register.html",
                              {"form": form},
                              context_instance=RequestContext(request))

def login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            auth_user = authenticate(username=data["username"],
                                     password=data["password"])
            django_login(request, auth_user)
            return HttpResponseRedirect(reverse("dashboard"))
    return render_to_response("accounts/login.html", {"form": form},
                              context_instance=RequestContext(request))

def logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse("accounts_login"))
