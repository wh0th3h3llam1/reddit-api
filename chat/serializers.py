from rest_framework import serializers

from common.mixins import SerializerCreateUpdateOnlyMixin
from core.serializers import DynamicFieldsModelSerializer

# Create your serializers here.


class ParticipantSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Participant
        fields = ("user", "room")


class RoomSerializer(DynamicFieldsModelSerializer):
    participants = serializers.IntegerField(source="get_participants_count")

    class Meta:
        model = Room
        fields = ("name", "participants")


class MessageSerializer(
    SerializerCreateUpdateOnlyMixin, DynamicFieldsModelSerializer
):
    class Meta:
        model = Message
        fields = "__all__"
