from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
import datetime
from ...models import OverallDriverPrediction, OverallConstructorPrediction, Race


class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **kwargs):
        email_list = []
        today = datetime.date.today()
        nearest_race = None
        for race in Race.objects.all():
            date_diff = today - race.start_date
            if date_diff.days != -1:
                return None
            nearest_race = race
        for prediction in OverallDriverPrediction.objects.all():
            if prediction.user.email:
                email_list.append(prediction.user.email)
        send_mail("Last day to record prediction for {0} GP".format(nearest_race.name),
                  render_to_string("race/email_reminder.txt",
                                   {"race": nearest_race,
                                    "site": Site.objects.get_current()}),
                  settings.DEFAULT_FROM_EMAIL,
                  email_list)
