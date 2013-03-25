from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.translation import ugettext as _

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User)
    token = models.CharField(max_length=36)

    created_on = models.DateField(auto_now_add = True)
    updated_on = models.DateField(auto_now = True)

    def __unicode__(self):
        return self.user.username

def send_password_reset(**kwargs):
    if kwargs["created"]:
        instance = kwargs["instance"]
        site = Site.objects.get_current()
        send_mail('Password reset for {0}'.format(site.name),
                  render_to_string('accounts/password_reset_email.txt',
                                   {"site": site,
                                    "password_token": instance.token}),
                  settings.DEFAULT_FROM_EMAIL, [instance.user.email],
                  fail_silently=False)
post_save.connect(send_password_reset, PasswordResetToken)
