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

    def save(self, **kwargs):
        user = super().save(**kwargs)
        user.set_password(self._validated_data.get('password'))
        user.save()
        return user

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