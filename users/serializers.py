from rest_framework import serializers
from rest_framework.authtoken.models import Token

from core.serializers import DynamicFieldsModelSerializer
from users.models import User

# Create your serializers here.


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    class Meta:
        model = Token
        fields = ("key", "username", "user")


class UserSerializer(DynamicFieldsModelSerializer):
    date_joined = serializers.DateTimeField(source="created")

    class Meta:
        model = User
        fields = ("id", "username", "email", "phone_number", "date_joined")
