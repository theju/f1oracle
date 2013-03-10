from .models import Driver, Constructor, Race
from django.shortcuts import render_to_response
from django.template import RequestContext

def dashboard(request):
    drivers = Driver.objects.all()
    constructors = Constructor.objects.all()
    races = Race.objects.all()
    return render_to_response("race/dashboard.html",
                              {"races": races,
                               "drivers": drivers,
                               "constructors": constructors},
                              context_instance=RequestContext(request))

def overall_driver_prediction(request):
    pass

def overall_constructor_prediction(request):
    pass

def race_driver_prediction(request, race_id=None):
    pass

def race_constructor_prediction(request, race_id=None):
    pass
