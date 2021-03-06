from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(label=_('Username'), max_length=30)
    password1 = forms.CharField(label=_('Password'),
                                max_length=20,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label=_('Confirm Password'),
                                max_length=20,
                                widget=forms.PasswordInput())
    email = forms.EmailField(label=_('Email (Optional)'), required=False)

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).count():
            raise forms.ValidationError(_("Username %(username)s "
                                          "already taken")
                                        % {"username": username})
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if email:
            if User.objects.filter(email=email).count():
                raise forms.ValidationError(_("Email address already taken"))
        return email

    def clean(self):
        if self.cleaned_data.get("password1") and \
                self.cleaned_data["password1"] != self.cleaned_data["password2"]:
            raise forms.ValidationError(_("Passwords do not match"))
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label=_('Username'), max_length=30)
    password = forms.CharField(label=_('Password'), max_length=20,
                               widget=forms.PasswordInput())

    def clean(self):
        try:
            user = User.objects.get(username=self.cleaned_data.get('username'))
        except User.DoesNotExist:
            raise forms.ValidationError(_("Username/Password did not match any of the "
                                          "records in our system"))
        if not user.check_password(self.cleaned_data.get("password")):
            raise forms.ValidationError(_("Username/Password did not match any of the "
                                          "records in our system"))
        return self.cleaned_data

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_('Email'))

    def clean(self):
        try:
            User.objects.get(email=self.cleaned_data.get("email"))
        except User.DoesNotExist:
            raise forms.ValidationError(_("No account seems to have been registered "
                                          "with this email address"))
        return self.cleaned_data

class PasswordChangeForm(forms.Form):
    token = forms.CharField(widget=forms.HiddenInput())
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        if self.cleaned_data.get("password1") and \
                self.cleaned_data["password1"] != self.cleaned_data["password2"]:
            raise forms.ValidationError(_("Passwords do not match"))
        return self.cleaned_data
