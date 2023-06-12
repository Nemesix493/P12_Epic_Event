from rest_framework.serializers import ModelSerializer

from ..models import SaleMember

class BaseSaleMemberSerializer(ModelSerializer):
    class Meta:
        model = SaleMember
        fields = [
            'username',
            'first_name',
            'last_name'
        ]


class WriteSaleMemberSerializer(BaseSaleMemberSerializer):
    class Meta(BaseSaleMemberSerializer.Meta):
        fields = [
            *BaseSaleMemberSerializer.Meta.fields,
            'email',
            'password'
        ]


class DetailsSaleMemberSerializer(BaseSaleMemberSerializer):
    class Meta(BaseSaleMemberSerializer.Meta):
        fields = [
            'id',
            *BaseSaleMemberSerializer.Meta.fields,
            'email',
            'groups'
        ]