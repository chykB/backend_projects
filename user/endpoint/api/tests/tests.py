from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import User, Organisation
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.utils import timezone
import jwt
from django.conf import settings


# Create your tests here.
class TokenGenerationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='jason@gmail.com', first_name='Jason', last_name='Malik', password='testpass123')
        self.client = APIClient()

    def test_token_expiration(self):
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])
        
        self.assertEqual(int(decoded_token["user_id"]), self.user.id)
        # self.assertEqual(decoded_token["email"], self.user.email)

class OrganisationAccessTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@gmail.com.com', first_name='User', last_name='One', password='testpass123')
        self.user2 = User.objects.create_user(email='user2@gmail.com.com', first_name='User', last_name='Two', password='testpass345')
        self.org1 = Organisation.objects.create(name="User One's Organisation")
        self.org2 = Organisation.objects.create(name="User Two's Organisation")
        self.org1.users.add(self.user1)
        self.org2.users.add(self.user2)
        self.client = APIClient()

    def test_user_own_organisation_only(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse("organisation-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "User One's Organisation")


    def test_user_cannot_access_other_organisation(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(reverse("organisation-detail", kwargs={"org_id": self.org2.org_id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        











