from django.core.management.base import BaseCommand
from django.conf import settings
from ...models import OverallDriverPrediction, OverallConstructorPrediction


class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **kwargs):
        conn = settings.REDIS_CONN
        num_ranks = conn.zcard("ranks")
        conn.zremrangebyscore("ranks", 0, num_ranks)
        for driver_prediction in OverallDriverPrediction.objects.all():
            conn.zadd("ranks",
                      driver_prediction.user.username,
                      driver_prediction.score)
        for constructor_prediction in OverallConstructorPrediction.objects.all():
            score = conn.zscore("ranks", constructor_prediction.user.username)
            if not score:
                score = 0
            conn.zadd("ranks",
                      constructor_prediction.user.username,
                      constructor_prediction.score + score)
