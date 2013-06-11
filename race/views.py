from .models import Driver, Constructor, Race, OverallDriverPredictionHistory, \
    OverallConstructorPredictionHistory, OverallConstructorPrediction, \
    OverallDriverPrediction, RaceDriverPrediction, RaceConstructorPrediction, \
    RaceUserWinner
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime

def index(request):
    return render_to_response("race/index.html", {},
                              context_instance=RequestContext(request))

@login_required
def dashboard(request):
    return render_to_response("race/dashboard.html", {},
                              context_instance=RequestContext(request))

@login_required
@require_POST
def overall_driver_prediction(request):
    if request.POST["driver_id"] == "-":
        messages.add_message(request, messages.ERROR,
                             _("Please select a valid driver"))
        return HttpResponseRedirect(reverse("dashboard"))
    try:
        driver = Driver.objects.get(id=request.POST["driver_id"])
    except DriverDoesNotExist:
        raise Http404
    driver_predictions = OverallDriverPredictionHistory.objects.filter(user=request.user).count()
    if driver_predictions >= 3:
        messages.add_message(request, messages.ERROR,
                             _("You've exceeded the maximum number of "
                               "tries to update the prediction"))
        return HttpResponseRedirect(reverse("dashboard"))
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
    messages.add_message(request, messages.SUCCESS,
                         _("You've successfully updated your prediction"))
    return HttpResponseRedirect(reverse("dashboard"))

@login_required
@require_POST
def overall_constructor_prediction(request):
    if request.POST["constructor_id"] == "-":
        messages.add_message(request, messages.ERROR,
                             _("Please select a valid constructor"))
        return HttpResponseRedirect(reverse("dashboard"))
    try:
        constructor = Constructor.objects.get(id=request.POST["constructor_id"])
    except ConstructorDoesNotExist:
        raise Http404
    constructor_predictions = OverallConstructorPredictionHistory.objects.filter(user=request.user).count()
    if constructor_predictions >= 3:
        messages.add_message(request, messages.ERROR,
                             _("You've exceeded the maximum number of "
                               "tries to update the prediction"))
        return HttpResponseRedirect(reverse("dashboard"))
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
    messages.add_message(request, messages.SUCCESS,
                         _("You've successfully updated your prediction"))
    return HttpResponseRedirect(reverse("dashboard"))

@login_required
@require_POST
def race_driver_prediction(request, race_id=None):
    try:
        race = Race.objects.get(id=race_id)
    except Race.DoesNotExist:
        raise Http404
    if request.POST["driver_id"] == "-":
        messages.add_message(request, messages.ERROR,
                             _("Please select a valid driver"))
        return HttpResponseRedirect(reverse("dashboard"))
    try:
        driver = Driver.objects.get(id=request.POST["driver_id"])
    except Driver.DoesNotExist:
        raise Http404
    if datetime.date.today() <= race.start_date:
        try:
            driver_prediction = RaceDriverPrediction.objects.get(user=request.user,
                                                                 race=race)
            driver_prediction.driver = driver
            driver_prediction.save()
        except RaceDriverPrediction.DoesNotExist:
            RaceDriverPrediction.objects.create(user=request.user,
                                                race=race,
                                                driver=driver)
        messages.add_message(request, messages.SUCCESS,
                             _("You've successfully updated your prediction"))
    return HttpResponseRedirect(reverse("dashboard"))

@login_required
@require_POST
def race_constructor_prediction(request, race_id=None):
    try:
        race = Race.objects.get(id=race_id)
    except Race.DoesNotExist:
        raise Http404
    if request.POST["constructor_id"] == "-":
        messages.add_message(request, messages.ERROR,
                             _("Please select a valid constructor"))
        return HttpResponseRedirect(reverse("dashboard"))
    try:
        constructor = Constructor.objects.get(id=request.POST["constructor_id"])
    except Constructor.DoesNotExist:
        raise Http404
    if datetime.date.today() <= race.start_date:
        try:
            constructor_prediction = RaceConstructorPrediction.objects.get(user=request.user,
                                                                           race=race)
            constructor_prediction.constructor = constructor
            constructor_prediction.save()
        except RaceConstructorPrediction.DoesNotExist:
            RaceConstructorPrediction.objects.create(user=request.user,
                                                     race=race,
                                                     constructor=constructor)
        messages.add_message(request, messages.SUCCESS,
                             _("You've successfully updated your prediction"))
    return HttpResponseRedirect(reverse("dashboard"))


@login_required
def scores(request):
    redis = settings.REDIS_CONN
    scores_list = []
    for rank, ii in enumerate(redis.zrevrange("ranks",
                                              0, 50, withscores=True)):
        scores_list.append({"rank": rank + 1,
                            "username": ii[0], "score": int(ii[1])})
    return render_to_response("race/scores.html",
                              {"scores": scores_list},
                              context_instance=RequestContext(request))

@login_required
def my_scores(request):
    redis = settings.REDIS_CONN
    my_standing = redis.zrevrank("ranks", request.user.username)
    if not my_standing:
        my_standing = 5

    scores_list = []
    for rank, ii in enumerate(redis.zrevrange("ranks",
                                              my_standing - 5,
                                              my_standing + 5,
                                              withscores=True)):
        scores_list.append({"rank": rank + 1,
                            "username": ii[0], "score": int(ii[1])})
    return render_to_response("race/scores.html",
                              {"scores": scores_list},
                              context_instance=RequestContext(request))


@login_required
def results(request):
    race_winners = RaceUserWinner.objects.all().order_by('-race__start_date')
    return render_to_response("race/results.html", {"race_winners": race_winners},
                              context_instance=RequestContext(request))
