from .forms import RegisterForm, LoginForm, PasswordResetForm, \
    PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, \
    login as django_login, logout as django_logout
from .models import PasswordResetToken
import uuid
from django.contrib import messages
from django.utils.translation import ugettext as _

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

def password_reset(request):
    form = PasswordResetForm()
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data["email"])
            PasswordResetToken.objects.create(user=user, token=str(uuid.uuid4()))
            messages.add_message(request, messages.SUCCESS,
                                 _("Password reset email has been sent successfully"))
    return render_to_response("accounts/password_reset.html", {"form": form},
                              context_instance=RequestContext(request))

def password_reset_confirm(request, token=None):
    if not token:
        messages.add_message(request, messages.ERROR,
                             _("Invalid Token"))
        return HttpResponseRedirect(reverse("accounts_login"))
    try:
        token = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        messages.add_message(request, messages.ERROR,
                             _("Invalid Token"))
        return HttpResponseRedirect(reverse("accounts_login"))
    form = PasswordChangeForm(initial={"token": token.token})
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            token.user.set_password(form.cleaned_data["password1"])
            token.user.save()
            token.delete()
            messages.add_message(request, messages.SUCCESS,
                                 _("Password has been successfully changed."))
            return HttpResponseRedirect(reverse("accounts_login"))
    return render_to_response("accounts/password_reset_form.html",
                              {"form": form,
                               "password_token": token.token},
                              context_instance=RequestContext(request))
