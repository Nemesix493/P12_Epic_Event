from rest_framework.serializers import ModelSerializer

from ..models import Event

class BaseEventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id',
            'event_date',
            'notes',
            'attendees',
            'event_status'
        ]

class WriteEventSerializer(BaseEventSerializer):
    pass

class ListEventSerializer(BaseEventSerializer):
    pass

class DetailEventSerializer(BaseEventSerializer):
    class Meta(BaseEventSerializer.Meta):
        fields = [
            *BaseEventSerializer.Meta.fields,
            'date_created',
            'date_updated'
        ]