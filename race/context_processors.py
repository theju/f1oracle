from .models import Driver, Constructor, Race, \
    OverallDriverPredictionHistory, OverallConstructorPredictionHistory, \
    OverallDriverPrediction, OverallConstructorPrediction
import datetime

def race_context_processor(request):
    if not request.user.is_authenticated():
        return {
            "today": datetime.date.today()
            }

    drivers = Driver.objects.all()
    constructors = Constructor.objects.all()
    races = Race.objects.all()

    driver_predictions = OverallDriverPredictionHistory.objects.filter(user=request.user).count()
    constructor_predictions = OverallConstructorPredictionHistory.objects.filter(user=request.user).count()
    num_tries_remaining = {"driver": 3 - driver_predictions,
                           "constructor": 3 - constructor_predictions}

    try:
        overall_driver_prediction = OverallDriverPrediction.objects.get(user=request.user)
    except OverallDriverPrediction.DoesNotExist:
        overall_driver_prediction = None
    try:
        overall_constructor_prediction = OverallConstructorPrediction.objects.get(user=request.user)
    except OverallConstructorPrediction.DoesNotExist:
        overall_constructor_prediction = None
    return {
        "races": races,
        "drivers": drivers,
        "constructors": constructors,
        "num_tries_remaining": num_tries_remaining,
        "overall_driver_prediction": overall_driver_prediction,
        "overall_constructor_prediction": overall_constructor_prediction,
        "today": datetime.date.today()
    }
