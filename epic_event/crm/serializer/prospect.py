from rest_framework.serializers import ModelSerializer

from ..models import Prospect

class BaseProspectSerializer(ModelSerializer):
    class Meta:
        model = Prospect
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'mobile',
            'company_name',
        ]

class WriteProspectSerializer(BaseProspectSerializer):
    pass

class ListProspectSerializer(BaseProspectSerializer):
    pass

class DetailProspectSerializer(BaseProspectSerializer):
    class Meta(BaseProspectSerializer.Meta):
        fields = [
            *BaseProspectSerializer.Meta.fields,
            'date_created',
            'date_updated'
        ]