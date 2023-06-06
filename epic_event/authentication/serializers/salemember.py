from .staffmember import BaseStaffMemberSerializer
from ..models import SaleMember

class BaseSaleMemberSerializer(BaseStaffMemberSerializer):
    class Meta(BaseStaffMemberSerializer.Meta):
        model = SaleMember


class WriteSaleMemberSerializer(BaseSaleMemberSerializer):
    class Meta(BaseSaleMemberSerializer.Meta):
        fields = [
            *BaseSaleMemberSerializer.Meta.fields,
            'email',
        ]


class DetailsSaleMemberSerializer(BaseSaleMemberSerializer):
    class Meta(BaseSaleMemberSerializer.Meta):
        fields = [
            'id',
            *BaseSaleMemberSerializer.Meta.fields,
            'email',
            'groups'
        ]