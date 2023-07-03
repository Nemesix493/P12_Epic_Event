from rest_framework.serializers import ModelSerializer

from ..models import Client
from authentication.exceptions import BadRequest
from authentication.models import SaleMember

class BaseClientSerializer(ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'mobile',
            'company_name',
        ]

class WriteClientSerializer(BaseClientSerializer):
    def save_with_sale_contact(self, sale_contact: SaleMember) -> Client:
        if not self.is_valid():
            raise BadRequest()
        client = self.Meta.model(sale_contact=sale_contact, **self.validated_data)
        client.save()
        self.instance=client
        return client

class ListClientSerializer(BaseClientSerializer):
    pass

class DetailClientSerializer(BaseClientSerializer):
    class Meta(BaseClientSerializer.Meta):
        fields = [
            *BaseClientSerializer.Meta.fields,
            'date_created',
            'date_updated'
        ]