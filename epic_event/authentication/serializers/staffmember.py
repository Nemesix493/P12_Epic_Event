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
    serializer_type = []
    def to_representation(self, instance):
        for type, serializer in self.serializer_type:
            if isinstance(instance.children, type):
                return serializer(instance.children).data
        return {}


class ListStaffMemberSerializer(BaseStaffMemberSerializer):
    class Meta(BaseStaffMemberSerializer.Meta):
        fields = [
            *BaseStaffMemberSerializer.Meta.fields,
            'id'
        ]
