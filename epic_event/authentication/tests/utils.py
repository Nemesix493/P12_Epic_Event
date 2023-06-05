from abc import ABC

from django.urls import reverse_lazy

from ..models import StaffMember


def get_user_test(member_type, username: str, password: str):
    if not member_type in [StaffMember, *StaffMember.__subclasses__()]:
        raise TypeError(f'{member_type.__name__} is not a subclass of StaffMember or StaffMember !')
    test_user = member_type.objects.create(
        username=username,
        email=f'{username}@epicevent.com',
        first_name='user',
        last_name='test',
        password=password
    )
    test_user.set_password(password)
    test_user.save()
    return test_user


class NeedToken(ABC):
    def get_user_token(self, username: str, password: str):
        response = self.client.post(
            path=reverse_lazy('authentication:token_obtain_pair'),
            data={
                'username': username,
                'password': password
            }
        )
        return response.json()