from abc import ABC

from django.urls import reverse_lazy

from ..models import StaffMember


class UserTokenMixin(ABC):
    @staticmethod
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
    
    def get_user_token(self, username: str, password: str):
        response = self.client.post(
            path=reverse_lazy('authentication:token_obtain_pair'),
            data={
                'username': username,
                'password': password
            }
        )
        return response.json()

    def do_as_response(self, do, as_class, args=[], kwargs={}) -> list:
        user_data = {
            'username': 'user_test',
            'password': 'password'
        }
        user_object = self.get_user_test(as_class, **user_data)
        user_token = self.get_user_token(**user_data)['access']
        result = do(token=user_token, *args, **kwargs)
        user_object.delete()
        return result

class DataBaseInitMixin(ABC):
    def init_db(self):
        from authentication.management.commands.init_groups import init_groups
        init_groups()