from .models import Driver, Constructor, Race, OverallDriverPredictionHistory, \
    OverallConstructorPredictionHistory, OverallConstructorPrediction, \
    OverallDriverPrediction
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import Http404
import datetime

@login_required
def dashboard(request):
    return render_to_response("race/dashboard.html", {},
                              context_instance=RequestContext(request))

@login_required
@require_POST
def overall_driver_prediction(request):
    try:
        driver = Driver.objects.get(id=request.POST["driver_id"])
    except DriverDoesNotExist:
        raise Http404
    context = {}
    driver_predictions = OverallDriverPredictionHistory.objects.filter(user=request.user).count()
    if driver_predictions >= 3:
        context["max_try_error"] = {"driver": True}
        return render_to_response("race/dashboard.html",
                                  context,
                                  context_instance=RequestContext(request))
    try:
        driver_prediction = OverallDriverPrediction.objects.get(user=request.user)
        if driver_prediction.driver != driver:
            driver_prediction.driver = driver
            driver_prediction.save()
        score = driver_prediction.score
    except OverallDriverPrediction.DoesNotExist:
        score = 0
        driver_prediction = OverallDriverPrediction.objects.create(user=request.user,
                                                                   driver=driver,
                                                                   score=score)
    OverallDriverPredictionHistory.objects.create(user=request.user,
                                                  driver=driver,
                                                  score=score)
    return render_to_response("race/dashboard.html",
                              context,
                              context_instance=RequestContext(request))

@login_required
@require_POST
def overall_constructor_prediction(request):
    try:
        constructor = Constructor.objects.get(id=request.POST["constructor_id"])
    except ConstructorDoesNotExist:
        raise Http404
    context = {}
    constructor_predictions = OverallConstructorPredictionHistory.objects.filter(user=request.user).count()
    if constructor_predictions >= 3:
        context["max_try_error"] = {"constructor": True}
        return render_to_response("race/dashboard.html",
                                  context,
                                  context_instance=RequestContext(request))
    try:
        constructor_prediction = OverallConstructorPrediction.objects.get(user=request.user)
        if constructor_prediction.constructor != constructor:
            constructor_prediction.constructor = constructor
            constructor_prediction.save()
        score = constructor_prediction.score
    except OverallConstructorPrediction.DoesNotExist:
        score = 0
        OverallConstructorPrediction.objects.create(user=request.user,
                                                    constructor=constructor,
                                                    score=0)
    OverallConstructorPredictionHistory.objects.create(user=request.user,
                                                       constructor=constructor,
                                                       score=score)
    return render_to_response("race/dashboard.html",
                              context,
                              context_instance=RequestContext(request))

@login_required
@require_POST
def race_driver_prediction(request, race_id=None):
    context = {}
    try:
        race = Race.objects.get(id=race_id)
    except Race.DoesNotExist:
        raise Http404
    if datetime.date.today() >= race.start_date:
        pass
    return render_to_response("race/dashboard.html",
                              context,
                              context_instance=RequestContext(request))

@login_required
@require_POST
def race_constructor_prediction(request, race_id=None):
    context = {}
    try:
        race = Race.objects.get(id=race_id)
    except Race.DoesNotExist:
        raise Http404
    if datetime.date.today() >= race.start_date:
        pass
    return render_to_response("race/dashboard.html",
                              context,
                              context_instance=RequestContext(request))
