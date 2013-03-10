from .forms import RegisterForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login

def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(username=data["username"],
                                            email=data.get("email", ""),
                                            password=data["password1"])
            auth_user = authenticate(username=user.username,
                                     password=data["password1"])
            django_login(request, auth_user)
            return HttpResponseRedirect(reverse("dashboard"))
    return render_to_response("accounts/register.html",
                              {"form": form},
                              context_instance=RequestContext(request))

def login(request):
    pass
