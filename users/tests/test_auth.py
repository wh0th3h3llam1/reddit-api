from django.test import TestCase
from rest_framework import status


class AuthenticationTest(TestCase):
    def setUp(self) -> None:
        self.signup_url = "/auth/signup/"
        self.login_url = "/auth/login/"

    def test_signup_user_empty(self):
        data = {}

        expected_response = {
            "username": ["This field is required."],
            "password1": ["This field is required."],
            "password2": ["This field is required."],
        }
        response = self.client.post(
            path=self.signup_url, data=data, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == expected_response

    def test_signup_user_password(self):
        data = {"username": "testuser", "password1": "", "password2": ""}

        expected_response = {
            "password1": ["This field may not be blank."],
            "password2": ["This field may not be blank."],
        }
        response = self.client.post(
            path=self.signup_url, data=data, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == expected_response

        data.update({"password1": "123", "password2": "123"})
        response = self.client.post(
            path=self.signup_url, data=data, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
