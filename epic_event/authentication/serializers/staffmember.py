from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.serializers import ModelSerializer, Serializer

from ..models import StaffMember

class BaseStaffMemberSerializer(ModelSerializer):
    class Meta:
        model = StaffMember
        fields = [
            'username',
            'first_name',
            'last_name'
        ]


class DetailsStaffMemberSerializer(Serializer):
    details_serializer_type = []
    def to_representation(self, instance):
        for model_class, serializer in self.details_serializer_type:
            if isinstance(instance, model_class):
                return serializer(instance).data
            elif hasattr(instance, 'children'):
                if isinstance(instance.children, model_class):
                    return serializer(instance.children).data
        raise APIException(f'Wrong type instance !', status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListStaffMemberSerializer(BaseStaffMemberSerializer):
    class Meta(BaseStaffMemberSerializer.Meta):
        fields = [
            *BaseStaffMemberSerializer.Meta.fields,
            'id'
        ]
