from io import BytesIO
from PIL import Image
from uuid import uuid4
from django.core.files.base import ContentFile

from django.core.files.uploadedfile import (
    SimpleUploadedFile,
)
import pytest

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase, override_settings
from common.utils import get_default_avatar_path

from users.tests.factories import UserFactory

# Create your tests here.


def get_temporary_file(
    filename="", content=b"content", content_type="image/jpg"
) -> SimpleUploadedFile:
    return SimpleUploadedFile(
        name=filename or f"file_{uuid4()}.jpg",
        content=content,
        content_type=content_type,
    )


def create_image(
    storage, filename, size=(100, 100), image_mode="RGB", image_format="PNG"
):
    """
    Generate a test image, returning the filename that it was saved as.

    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
    """
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)


class LoggedInTestCase(APITestCase):
    fixtures = []

    def setUp(self) -> None:
        self.client = APIClient()

        self.admin = UserFactory()
        self.admin_detail = reverse("users-detail", args=[self.admin.username])
        self.client.force_login(user=self.admin)


class TestUserViewSetUnauthenticated(LoggedInTestCase):
    """Test UserViewSet as unauthenticated user"""

    fixtures = []

    def setUp(self) -> None:
        super().setUp()
        self.client.logout()

    def test_get_user(self):
        response = self.client.get(self.admin_detail)
        assert response.status_code == status.HTTP_200_OK

    def test_patch_user_fail(self):
        data = {"phone_number": "+919876543210"}
        response = self.client.patch(path=self.admin_detail, data=data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_user_fail(self):
        response = self.client.delete(path=self.admin_detail)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_change_avatar_user_fail(self):
        data = {"avatar": get_temporary_file()}
        response = self.client.post(
            path=reverse("users-avatar", args=[self.admin.username]), data=data
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_change_username_user_fail(self):
        data = {"username": "new_random_username"}
        response = self.client.post(
            path=reverse("users-change-username", args=[self.admin.username]),
            data=data,
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestUserViewSet(LoggedInTestCase):
    """Test UserViewSet as authenticated user"""

    def setUp(self) -> None:
        super().setUp()

        self.user = UserFactory(username="morpankh", email="morpankh@test.me")
        self.user_detail = reverse("users-detail", args=[self.user.username])
        self.client.force_authenticate(user=self.user)

    def test_get_user(self):
        response = self.client.get(self.user_detail)
        assert response.status_code == status.HTTP_200_OK

    def test_patch_user(self):
        data = {"phone_number": "9876543210"}
        response = self.client.patch(path=self.admin_detail, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = self.client.patch(path=self.user_detail, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        data["phone_number"] = "+919876543210"
        response = self.client.patch(path=self.user_detail, data=data)
        assert response.status_code == status.HTTP_200_OK

    def test_delete_user(self):
        response = self.client.delete(path=self.admin_detail)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = self.client.delete(path=self.user_detail)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.skip(reason="Empty File Error")
    def test_change_avatar_user(self):
        file = get_temporary_file()
        file.seek(0)
        data = {}
        response = self.client.post(
            path=reverse("users-avatar", args=[self.admin.username]),
            data=data,
            format="multipart",
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # empty avatar
        response = self.client.post(
            path=reverse("users-avatar", args=[self.user.username]),
            data=data,
            format="multipart",
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["avatar"] is not None

        # change avatar
        avatar = create_image(None, "avatar.png")

        avatar_file = get_temporary_file(
            "avatar.png", avatar.getvalue(), "image/png"
        )
        avatar_file.seek(0)
        data["avatar"] = avatar_file
        response = self.client.post(
            path=reverse("users-avatar", args=[self.user.username]),
            data=data,
            format="multipart",
        )
        assert response.status_code == status.HTTP_200_OK
        assert f"{self.user.username}/avatar" in response.json()["avatar"]

        # remove avatar
        data["remove"] = True
        response = self.client.post(
            path=reverse("users-avatar", args=[self.user.username]),
            data=data,
            format="multipart",
        )
        assert response.status_code == status.HTTP_200_OK
        assert get_default_avatar_path() in response.json()["avatar"]

    @override_settings(USERNAME_CHANGE_ALLOWED_AFTER=14)
    def test_change_username_user(self):
        new_username = "new_random_username"
        data = {"username": new_username}
        response = self.client.post(
            path=reverse("users-change-username", args=[self.admin.username]),
            data=data,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        response = self.client.post(
            path=reverse("users-change-username", args=[self.user.username]),
            data=data,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["confirm"] == ["Confirm username change"]

        data["confirm"] = True
        response = self.client.post(
            path=reverse("users-change-username", args=[self.user.username]),
            data=data,
        )
        assert response.status_code == status.HTTP_200_OK

        response = self.client.get(
            path=reverse("users-detail", args=[self.user.username])
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

        response = self.client.post(
            path=reverse("users-change-username", args=[new_username]),
            data=data,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert ["Username not available"] in response.json().values()

        data["username"] = "random_usernamme123s"
        response = self.client.post(
            path=reverse("users-change-username", args=[new_username]),
            data=data,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # assert [
        #     "You must wait for at least 14 days days before changing username again."
        # ] in response.json().values()
