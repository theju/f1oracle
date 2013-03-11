from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from rq import Queue
from redis import Redis
from django.conf import settings

class Country(models.Model):
    name = models.CharField(max_length=50)
    iso_code = models.CharField(max_length=2)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ["name"]


class Race(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["start_date"]


class Constructor(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Driver(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey(Country)
    constructor = models.ForeignKey(Constructor)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["id"]


class Result(models.Model):
    race = models.ForeignKey(Race)
    driver = models.ForeignKey(Driver)
    points = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return _("%(race)s : %(driver)s earned "
                 "%(points)d points") % {"race": self.race,
                                         "driver": self.driver,
                                         "points": self.points}


class RaceDriverPrediction(models.Model):
    user = models.ForeignKey(User)
    race = models.ForeignKey(Race)
    driver = models.ForeignKey(Driver)
    score = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return _("%(username)s : %(race)s -> "
                 "%(score)d points") % {"username": self.user.username,
                                        "race": self.race,
                                        "score": self.score}


class RaceConstructorPrediction(models.Model):
    user = models.ForeignKey(User)
    race = models.ForeignKey(Race)
    constructor = models.ForeignKey(Constructor)
    score = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return _("%(username)s : %(race)s -> "
                 "%(score)d points") % {"username": self.user.username,
                                        "race": self.race,
                                        "score": self.score}


class OverallDriverPrediction(models.Model):
    user = models.ForeignKey(User)
    driver = models.ForeignKey(Driver)
    score = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return _("%(username)s : %(driver)s -> "
                 "%(score)d points") % {"username": self.user.username,
                                        "driver": self.driver,
                                        "score": self.score}


class OverallConstructorPrediction(models.Model):
    user = models.ForeignKey(User)
    constructor = models.ForeignKey(Constructor)
    score = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return _("%(usename)s : %(constructor)s -> "
                 "%(score)d points") % {"username": self.user.username,
                                        "constructor": self.constructor,
                                        "score": self.score}


class OverallDriverPredictionHistory(models.Model):
    user = models.ForeignKey(User)
    driver = models.ForeignKey(Driver)
    score = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return _("%(username)s : %(driver)s -> "
                 "%(score)d points") % {"username": self.user.username,
                                        "driver": self.driver,
                                        "score": self.score}


class OverallConstructorPredictionHistory(models.Model):
    user = models.ForeignKey(User)
    constructor = models.ForeignKey(Constructor)
    score = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return _("%(username)s : %(constructor)s -> "
                 "%(score)d points") % {"username": self.user.username,
                                        "constructor": self.constructor,
                                        "score": self.score}


class RaceUserWinner(models.Model):
    user = models.ForeignKey(User)
    race = models.ForeignKey(Race)
    driver = models.ForeignKey(Driver)
    constructor = models.ForeignKey(Constructor)

    def __unicode__(self):
        return _("%(username)s is winner "
                 "of %(race)s") % {"username": self.user.username,
                                   "race": self.race}


def update_scores(instance):
    for prediction in RaceDriverPrediction.objects.filter(driver=instance.driver):
        prediction.score += instance.points
        prediction.save()
    for prediction in OverallDriverPrediction.objects.filter(driver=instance.driver):
        prediction.score += instance.points
        prediction.save()
    for prediction in RaceConstructorPrediction.objects.filter(constructor=instance.driver.constructor):
        prediction.score += instance.points
        prediction.save()
    for prediction in OverallConstructorPrediction.objects.filter(constructor=instance.driver.constructor):
        prediction.score += instance.points
        prediction.save()

# Signal handlers
def update_scores_signal_handler(**kwargs):
    if kwargs["created"]:
        redis_conn = Redis()
        queue_kwargs = {"connection": redis_conn}
        if settings.DEBUG == True:
            queue_kwargs.update({"async": False})
        qu = Queue(**queue_kwargs)
        qu.enqueue(update_scores, kwargs["instance"])
post_save.connect(update_scores_signal_handler, Result)
