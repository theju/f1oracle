import datetime
import urlparse
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from .models import Race, Driver, Constructor, Result, \
    RaceDriverPrediction, OverallDriverPrediction, \
    OverallConstructorPrediction, RaceConstructorPrediction, \
    OverallDriverPredictionHistory, OverallConstructorPredictionHistory, \
    RaceUserWinner
from django.conf import settings


class RaceTestCase(TestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        settings.DEBUG = True

    def tearDown(self):
        settings.DEBUG = False

    def create_user(self, username, password, email=None):
        return User.objects.create_user(username=username,
                                        email=email,
                                        password=password)

    def test_signup(self):
        post_data = {
            "username": "",
            "password1": "",
            "password2": "",
            "email": ""
            }
        response = self.client.post("/accounts/register/", post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors != {})
        self.assertTrue(response.context["form"].errors.keys() \
                            == ["username", "password1", "password2"])
        new_post_data = post_data.copy()
        new_post_data["username"] = "foo"
        new_post_data["password1"] = "bar"
        new_post_data["password2"] = "bar"
        response = self.client.post("/accounts/register/", new_post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)
        new_post_data = post_data.copy()
        new_post_data["username"] = "foo"
        new_post_data["password1"] = "bar"
        new_post_data["password2"] = "bar1"
        response = self.client.post("/accounts/register/", new_post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors != {})
        self.assertEqual(User.objects.count(), 1)
        new_post_data["username"] = "foo"
        new_post_data["password1"] = "bar123"
        new_post_data["password2"] = "bar123"
        response = self.client.post("/accounts/register/", new_post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors.keys(), ["username"])
        self.assertEqual(User.objects.count(), 1)
        new_post_data["username"] = "foo1"
        new_post_data["password1"] = "bar123"
        new_post_data["password2"] = "bar123"
        new_post_data["email"] = "foo@example.com"
        response = self.client.post("/accounts/register/", new_post_data)
        self.assertEqual(response.status_code, 302)
        redirect_url = response["Location"]
        redirect_url_parsed = urlparse.urlparse(redirect_url)
        self.assertEqual(redirect_url_parsed.path, reverse("dashboard"))
        self.assertEqual(User.objects.count(), 2)
        new_user = User.objects.get(username=new_post_data["username"])
        self.assertEqual(new_user.email, new_post_data["email"])

    def test_login(self):
        post_data = {"username": "", "password": ""}
        response = self.client.post("/accounts/login/", post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors.keys() \
                            == ["username", "password", "__all__"])
        post_data = {"username": "", "password": "bar123"}
        response = self.client.post("/accounts/login/", post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors.keys() \
                            == ["username", "__all__"])
        post_data = {"username": "foo", "password": ""}
        response = self.client.post("/accounts/login/", post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors.keys() \
                            == ["password", "__all__"])
        post_data = {"username": "foo", "password": "bar"}
        self.create_user(**post_data)
        response = self.client.post("/accounts/login/", post_data)
        self.assertEqual(response.status_code, 302)
        redirect_url = response["Location"]
        redirect_url_parsed = urlparse.urlparse(redirect_url)
        self.assertEqual(redirect_url_parsed.path, reverse("dashboard"))

    def test_forgot_password(self):
        # TODO: Add later
        pass

    def test_add_overall_driver_prediction(self):
        auth_kwargs = {"username": "foo1", "password": "bar1"}
        user = self.create_user(**auth_kwargs)
        self.client.login(**auth_kwargs)
        driver_id = 5
        response = self.client.post("/dashboard/overall_race/driver/",
                                    {"driver_id": driver_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OverallDriverPrediction.objects.count(), 1)
        user_prediction = OverallDriverPrediction.objects.get()
        self.assertEqual(user_prediction.driver.id, driver_id)
        self.assertEqual(user_prediction.score, 0)
        self.assertEqual(user_prediction.user, user)

        race1 = Race.objects.get(id=1)
        race2 = Race.objects.get(id=2)
        result = Result.objects.create(race=race1,
                                       driver=user_prediction.driver,
                                       points=18)
        user_prediction = OverallDriverPrediction.objects.get()
        self.assertEqual(user_prediction.score, 18)
        result = Result.objects.create(race=race2,
                                       driver=user_prediction.driver,
                                       points=25)
        user_prediction = OverallDriverPrediction.objects.get()
        self.assertEqual(user_prediction.score, 43)

    def test_overall_driver_prediction_exceed_max_tries(self):
        auth_kwargs = {"username": "foo1", "password": "bar1"}
        user = self.create_user(**auth_kwargs)
        self.client.login(**auth_kwargs)
        driver_id = 5
        for ii in range(4):
            response = self.client.post("/dashboard/overall_race/driver/",
                                        {"driver_id": driver_id + ii})
            self.assertEqual(response.status_code, 200)
        user_prediction = OverallDriverPrediction.objects.get(user=user)
        self.assertEqual(user_prediction.driver.id, 7)
        self.assertEqual(OverallDriverPredictionHistory.objects.count(), 3)
    
    def test_add_overall_constructor_prediction(self):
        auth_kwargs = {"username": "foo1", "password": "bar1"}
        user = self.create_user(**auth_kwargs)
        self.client.login(**auth_kwargs)
        constructor_id = 2
        response = self.client.post("/dashboard/overall_race/constructor/",
                                    {"constructor_id": constructor_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OverallConstructorPrediction.objects.filter(user=user).count(), 1)
        user_prediction = OverallConstructorPrediction.objects.get(user=user)
        self.assertEqual(user_prediction.constructor.id, constructor_id)
        self.assertEqual(user_prediction.score, 0)
        self.assertEqual(user_prediction.user, user)

        driver1 = Driver.objects.get(id=3)
        driver2 = Driver.objects.get(id=4)
        race1 = Race.objects.get(id=1)
        race2 = Race.objects.get(id=2)
        result = Result.objects.create(race=race1,
                                       driver=driver1,
                                       points=18)
        user_prediction = OverallConstructorPrediction.objects.get(user=user)
        self.assertEqual(user_prediction.score, 18)
        result = Result.objects.create(race=race1,
                                       driver=driver2,
                                       points=25)
        result = Result.objects.create(race=race2,
                                       driver=driver1,
                                       points=10)
        user_prediction = OverallConstructorPrediction.objects.get(user=user)
        self.assertEqual(user_prediction.score, 53)
        result = Result.objects.create(race=race2,
                                       driver=driver2,
                                       points=18)
        user_prediction = OverallConstructorPrediction.objects.get(user=user)
        self.assertEqual(user_prediction.score, 71)
        constructor_id = 2
        response = self.client.post("/dashboard/overall_race/constructor/",
                                    {"constructor_id": constructor_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OverallConstructorPrediction.objects.filter(user=user).count(), 1)
        self.assertEqual(OverallConstructorPredictionHistory.objects.filter(user=user).count(), 2)
        user_prediction = OverallConstructorPrediction.objects.get(user=user)
        self.assertEqual(user_prediction.score, 71)

        auth_kwargs = {"username": "foo2", "password": "bar1"}
        user = self.create_user(**auth_kwargs)
        self.client.login(**auth_kwargs)
        constructor_id = 5
        response = self.client.post("/dashboard/overall_race/constructor/",
                                    {"constructor_id": constructor_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OverallConstructorPrediction.objects.filter(user=user).count(), 1)
        user_prediction = OverallConstructorPrediction.objects.get(user=user)
        self.assertEqual(user_prediction.constructor.id, constructor_id)
        self.assertEqual(user_prediction.score, 0)
        self.assertEqual(user_prediction.user, user)

        driver1 = Driver.objects.get(id=3)
        driver2 = Driver.objects.get(id=4)
        race1 = Race.objects.get(id=1)
        race2 = Race.objects.get(id=2)
        result = Result.objects.create(race=race1,
                                       driver=driver1,
                                       points=18)
        user_prediction = OverallConstructorPrediction.objects.get(user=user)
        self.assertEqual(user_prediction.score, 0)
        result = Result.objects.create(race=race1,
                                       driver=driver2,
                                       points=25)
        result = Result.objects.create(race=race2,
                                       driver=driver1,
                                       points=10)
        user_prediction = OverallConstructorPrediction.objects.get(user=user)
        self.assertEqual(user_prediction.score, 0)
        result = Result.objects.create(race=race2,
                                       driver=driver2,
                                       points=18)
        user_prediction = OverallConstructorPrediction.objects.get(user=user)
        self.assertEqual(user_prediction.score, 0)
        constructor_id = 2
        response = self.client.post("/dashboard/overall_race/constructor/",
                                    {"constructor_id": constructor_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(OverallConstructorPrediction.objects.filter(user=user).count(), 1)
        self.assertEqual(OverallConstructorPredictionHistory.objects.filter(user=user).count(), 2)
        user_prediction = OverallConstructorPrediction.objects.get(user=user)
        self.assertEqual(user_prediction.score, 0)

    def test_overall_constructor_exceed_max_tries(self):
        auth_kwargs = {"username": "foo1", "password": "bar1"}
        user = self.create_user(**auth_kwargs)
        self.client.login(**auth_kwargs)
        constructor_id = 5
        for ii in range(4):
            response = self.client.post("/dashboard/overall_race/constructor/",
                                        {"constructor_id": constructor_id + ii})
        user_prediction = OverallConstructorPrediction.objects.get(user=user)
        self.assertEqual(user_prediction.constructor.id, 7)
        self.assertEqual(OverallConstructorPredictionHistory.objects.count(), 3)

    def test_race1_driver_prediction(self):
        auth_kwargs = {"username": "foo1", "password": "bar1"}
        user = self.create_user(**auth_kwargs)
        self.client.login(**auth_kwargs)
        driver_id = 5
        response = self.client.post("/dashboard/race1/driver/",
                                    {"driver_id": driver_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(RaceDriverPrediction.objects.count(), 1)
        user_prediction = RaceDriverPrediction.objects.get()
        self.assertEqual(user_prediction.race.country.iso_code, "AU")
        self.assertEqual(user_prediction.driver.id, driver_id)
        self.assertEqual(user_prediction.score, 0)
        self.assertEqual(user_prediction.user, user)

        result = Result.objects.create(race=user_prediction.race,
                                       driver=user_prediction.driver,
                                       points=18)
        user_prediction = RaceDriverPrediction.objects.get()
        self.assertEqual(user_prediction.score, 18)        

    def test_race1_constructor_prediction(self):
        auth_kwargs = {"username": "foo1", "password": "bar1"}
        user = self.create_user(**auth_kwargs)
        self.client.login(**auth_kwargs)
        constructor_id = 2
        response = self.client.post("/dashboard/race1/constructor/",
                                    {"constructor_id": constructor_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(RaceConstructorPrediction.objects.count(), 1)
        user_prediction = RaceConstructorPrediction.objects.get()
        self.assertEqual(user_prediction.race.country.iso_code, "AU")
        self.assertEqual(user_prediction.constructor.id, constructor_id)
        self.assertEqual(user_prediction.score, 0)
        self.assertEqual(user_prediction.user, user)        

        driver1 = Driver.objects.get(id=4)
        driver2 = Driver.objects.get(id=3)
        result = Result.objects.create(race=user_prediction.race,
                                       driver=driver1,
                                       points=18)
        result = Result.objects.create(race=user_prediction.race,
                                       driver=driver2,
                                       points=25)
        user_prediction = RaceConstructorPrediction.objects.get()
        self.assertEqual(user_prediction.score, 43)
