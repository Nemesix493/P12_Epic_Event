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

    def save(self, **kwargs):
        user = super().save(**kwargs)
        user.set_password(self._validated_data.get('password'))
        user.save()
        return user

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