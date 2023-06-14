from rest_framework.serializers import ModelSerializer

from ..models import ManageMember

class BaseManageMemberSerializer(ModelSerializer):
    class Meta:
        model = ManageMember
        fields = [
            'username',
            'first_name',
            'last_name'
        ]


class WriteManageMemberSerializer(BaseManageMemberSerializer):
    class Meta(BaseManageMemberSerializer.Meta):
        fields = [
            *BaseManageMemberSerializer.Meta.fields,
            'email',
            'password'
        ]


class DetailsManageMemberSerializer(BaseManageMemberSerializer):
    class Meta(BaseManageMemberSerializer.Meta):
        fields = [
            'id',
            *BaseManageMemberSerializer.Meta.fields,
            'email',
            'groups'
        ]