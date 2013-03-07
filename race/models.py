from django.db import models
from django.contrib.auth.models import User

class Country(models.Model):
    name = models.CharField(max_length=50)
    iso_code = models.CharField(max_length=2)

    def __unicode__(self):
        return self.name


class Race(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return self.name


class Constructor(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return self.name


class Driver(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey(Country)
    constructor = models.ForeignKey(Constructor)

    def __unicode__(self):
        return self.name


class Result(models.Model):
    race = models.ForeignKey(Race)
    driver = models.ForeignKey(Driver)
    points = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{0} : {1} earned {2} points".format(self.race,
                                                    self.driver,
                                                    self.points)


class RaceDriverPrediction(models.Model):
    user = models.ForeignKey(User)
    race = models.ForeignKey(Race)
    driver = models.ForeignKey(Driver)
    score = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{0} : {1} -> {2} points".format(self.user.username,
                                                self.race,
                                                self.score)


class OverallDriverPrediction(models.Model):
    user = models.ForeignKey(User)
    driver = models.ForeignKey(Driver)
    score = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{0} : {1} -> {2} points".format(self.user.username,
                                                self.driver,
                                                self.score)


class OverallConstructorPrediction(models.Model):
    user = models.ForeignKey(User)
    constructor = models.ForeignKey(Constructor)
    score = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{0} : {1} -> {2} points".format(self.user.username,
                                                self.constructor,
                                                self.score)

class OverallDriverPredictionHistory(models.Model):
    user = models.ForeignKey(User)
    driver = models.ForeignKey(Driver)
    score = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{0} : {1} -> {2} points".format(self.user.username,
                                                self.driver,
                                                self.score)


class OverallConstructorPredictionHistory(models.Model):
    user = models.ForeignKey(User)
    constructor = models.ForeignKey(Constructor)
    score = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "{0} : {1} -> {2} points".format(self.user.username,
                                                self.constructor,
                                                self.score)
