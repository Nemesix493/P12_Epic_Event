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

    def save(self, **kwargs):
        user = super().save(**kwargs)
        user.set_password(self._validated_data.get('password'))
        user.save()
        return user
    
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