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
        # password blank
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

        # password doesn't match
        data.update({"password1": "123#@456", "password2": "abckj@4569"})
        expected_response = {
            "non_field_errors": ["The two password fields didn't match."]
        }
        response = self.client.post(
            path=self.signup_url, data=data, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == expected_response

        # password short and numeric
        data.update({"password1": "123", "password2": "123"})
        expected_response = {
            "password1": [
                "This password is too short. It must contain at least 8 characters.",
                "This password is too common.",
                "This password is entirely numeric.",
            ]
        }
        response = self.client.post(
            path=self.signup_url, data=data, format="json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == expected_response

    def test_signup_user_username(self):
        data = {
            "username": "test",
            "password1": "ARandomPassword@123",
            "password2": "ARandomPassword@123",
        }

        response = self.client.post(
            path=self.signup_url,
            data=data,
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["username"] == [
            "Username must have at least 5 characters"
        ]

    def test_signup_user(self):
        data = {
            "username": "testuser",
            "password1": "ARandomPassword@123",
            "password2": "ARandomPassword@123",
        }

        response = self.client.post(
            path=self.signup_url,
            data=data,
            format="json",
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert "key" in response.json()
        assert "username" in response.json()

    def test_login_user_fail(self):
        data = {}

        response = self.client.post(
            path=self.login_url,
            data=data,
            format="json",
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"password": ["This field is required."]}

        data = {"password": "pass"}
        response = self.client.post(
            path=self.login_url,
            data=data,
            format="json",
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["non_field_errors"] == [
            'Must include "username" and "password".'
        ]

        data = {"username": "user", "password": "pass"}
        response = self.client.post(
            path=self.login_url,
            data=data,
            format="json",
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["non_field_errors"] == [
            "Unable to log in with provided credentials."
        ]

    def test_login_user(self):
        data = {
            "username": "testuser",
            "password1": "ARandomPassword@123",
            "password2": "ARandomPassword@123",
        }

        response = self.client.post(
            path=self.signup_url,
            data=data,
            format="json",
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED

        data = {"username": "testuser", "password": "ARandomPassword@123"}
        response = self.client.post(
            path=self.login_url,
            data=data,
            format="json",
            content_type="application/json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert "key" in response.json()
        assert "username" in response.json()
