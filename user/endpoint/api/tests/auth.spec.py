from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import User, Organisation

class AuthEneToEndTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")
        self.login_url = reverse("login")

    def register_user_successfully(self):
        data = {
            "email": "kosi@gmail.com",
            "first_name": "Jasmine",
            "last_name": "Malik",
            "password": "kosi1234"

        }

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["message"], "Registration successful")
        self.assertIn("accessToken", response.data["data"])
        self.assertEqual(response.data["data"],["user"],["first_name"], "Jason")
        self.assertEqual(response.data["data"],["user"],["last_name"], "Malik")
        self.assertEqual(response.data["data"],["user"],["email"], "jason@gmail.com")


        user = User.objects.get("jason@gmail.com")
        org = Organisation.objects.get(users=user)
        self.assertEqual(org.name, "Jason's Organisation")


    def test_login_user_successfully(self):
        register_data = {
            "email": "ben@gmail.com",
            "first_name": "Ben",
            "last_name": "Jon",
            "password": "benjon123"
        }

        login_data = {
            "email": "ben@gmail.com",
            "password": "benjon123"
        }

        response = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["message"], "Login successfully")
        self.assertIn("accessToken", response.data["data"])
        self.assertEqual(response.data["data"],["user"],["email"], "ben@gmail.com")


    def test_register_fail_missing_fields(self):
        required_fields = ["email", "first_name", "last_name", "password"]
        for field in required_fields:
            data = {
                "email": "mark@gmail.com",
                "first_name": "Mark",
                "last_name": "Ray",
                "password": "markray123" 
            }
            data.pop(field)
            response = self.client.post(self.register_url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
            self.assertIn("errors", response.data)
            self.assertIn(field, response.data["errors"])


    def test_register_fail_duplicate_email(self):
        data = {
            "email": "james@gmail.com",
            "first_name": "James",
            "last_name": "King",
            "password": "jamesking123"
        }

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        self.assertIn("errors", response.data)
        self.assertIn("email", response.data['errors'])



