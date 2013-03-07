from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from .models import Race, Driver, Constructor, Result, \
    RaceDriverPrediction, OverallDriverPrediction, \
    OverallConstructorPrediction, RaceConstructorPrediction, \
    OverallDriverPredictionHistory, OverallConstructorPredictionHistory, \
    RaceWinner


class AuthTest(TestCase):
    def test_signup(self):
        post_data = {
            "username": "",
            "password": "",
            "email": ""
            }
        response = self.client.post("/accounts/register/", post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors != {})
        self.assertTrue(response.context["form"].errors.keys() == ["username", "password"])
        new_post_data = post_data.copy()
        new_post_data["username"] = "foo"
        new_post_data["password"] = "bar"
        response = self.client.post("/accounts/register/", new_post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors == {})
        self.assertEqual(User.objects.count(), 1)
        new_post_data["username"] = "foo"
        new_post_data["password"] = "bar123"
        response = self.client.post("/accounts/register/", new_post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors.keys(), ["username"])
        self.assertEqual(User.objects.count(), 1)
        new_post_data["username"] = "foo1"
        new_post_data["password"] = "bar123"
        new_post_data["email"] = "foo@example.com"
        response = self.client.post("/accounts/register/", new_post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 2)
        new_user = User.objects.get(username=new_post_data["username"])
        self.assertEqual(new_user.email, new_post_data["email"])

    def test_login(self):
        post_data = {"username": "", "password": ""}
        response = self.client.post("/accounts/login/", post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors.keys() == ["username", "password"])
        post_data = {"username": "", "password": "bar123"}
        response = self.client.post("/accounts/login/", post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors.keys() == ["username"])
        post_data = {"username": "foo", "password": ""}
        response = self.client.post("/accounts/login/", post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors.keys() == ["password"])
        post_data = {"username": "foo", "password": "bar123"}
        response = self.client.post("/accounts/register/", post_data)
        response = self.client.post("/accounts/login/", post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("dashboard_index"))

    def test_forgot_password(self):
        # TODO: Add later
        pass

    def test_add_overall_driver_prediction(self):
        pass

    def test_overall_driver_prediction_exceed_max_tries(self):
        pass
    
    def test_add_overall_constructor_prediction(self):
        pass

    def test_overall_constructor_exceed_max_tries(self):
        pass

    def test_race1_driver_prediction(self):
        pass

    def test_race1_constructor_prediction(self):
        pass
