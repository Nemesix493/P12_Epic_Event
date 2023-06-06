from .staffmember import BaseStaffMemberSerializer
from ..models import SupportMember

class BaseSupportMemberSerializer(BaseStaffMemberSerializer):
    class Meta(BaseStaffMemberSerializer.Meta):
        model = SupportMember


class WriteSupportMemberSerializer(BaseSupportMemberSerializer):
    class Meta(BaseSupportMemberSerializer.Meta):
        fields = [
            *BaseSupportMemberSerializer.Meta.fields,
            'email',
        ]


class DetailsSupportMemberSerializer(BaseSupportMemberSerializer):
    class Meta(BaseSupportMemberSerializer.Meta):
        fields = [
            'id',
            *BaseSupportMemberSerializer.Meta.fields,
            'email',
            'groups'
        ]