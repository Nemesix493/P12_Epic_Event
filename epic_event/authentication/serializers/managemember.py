from .staffmember import BaseStaffMemberSerializer
from ..models import ManageMember

class BaseManageMemberSerializer(BaseStaffMemberSerializer):
    class Meta(BaseStaffMemberSerializer.Meta):
        model = ManageMember


class WriteManageMemberSerializer(BaseManageMemberSerializer):
    class Meta(BaseManageMemberSerializer.Meta):
        fields = [
            *BaseManageMemberSerializer.Meta.fields,
            'email',
        ]


class DetailsManageMemberSerializer(BaseManageMemberSerializer):
    class Meta(BaseManageMemberSerializer.Meta):
        fields = [
            'id',
            *BaseManageMemberSerializer.Meta.fields,
            'email',
            'groups'
        ]