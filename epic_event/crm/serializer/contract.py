from rest_framework.serializers import ModelSerializer

from ..models import Contract

class BaseContractSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            'id',
            'amount',
            'payment_due',
            'status',
            'client'
        ]

class WriteContractSerializer(BaseContractSerializer):
    pass

class ListContractSerializer(BaseContractSerializer):
    pass

class DetailContractSerializer(BaseContractSerializer):
    class Meta(BaseContractSerializer.Meta):
        fields = [
            *BaseContractSerializer.Meta.fields,
            'date_created',
            'date_updated'
        ]