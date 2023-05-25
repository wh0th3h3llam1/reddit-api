from rest_framework import serializers
from core.serializers import DynamicFieldsModelSerializer
from users.models import User

# Create your serializers here.


class UserSerializer(DynamicFieldsModelSerializer):
    date_joined = serializers.DateTimeField(source="created")

    class Meta:
        model = User
        fields = ("id", "username", "email", "phone_number", "date_joined")
