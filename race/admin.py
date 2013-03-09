from django.contrib import admin
from .models import Country, Race, Constructor, Driver, Result, \
    RaceDriverPrediction, RaceConstructorPrediction, OverallDriverPrediction, \
    OverallConstructorPrediction, OverallDriverPredictionHistory, \
    OverallConstructorPredictionHistory, RaceUserWinner

admin.site.register(Country)
admin.site.register(Race)
admin.site.register(Constructor)
admin.site.register(Driver)
