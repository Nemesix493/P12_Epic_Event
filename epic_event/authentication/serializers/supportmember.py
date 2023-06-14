from rest_framework.serializers import ModelSerializer

from ..models import SupportMember

class BaseSupportMemberSerializer(ModelSerializer):
    class Meta:
        model = SupportMember
        fields = [
            'username',
            'first_name',
            'last_name'
        ]


class WriteSupportMemberSerializer(BaseSupportMemberSerializer):
    class Meta(BaseSupportMemberSerializer.Meta):
        fields = [
            *BaseSupportMemberSerializer.Meta.fields,
            'email',
            'password'
        ]


class DetailsSupportMemberSerializer(BaseSupportMemberSerializer):
    class Meta(BaseSupportMemberSerializer.Meta):
        fields = [
            'id',
            *BaseSupportMemberSerializer.Meta.fields,
            'email',
            'groups'
        ]