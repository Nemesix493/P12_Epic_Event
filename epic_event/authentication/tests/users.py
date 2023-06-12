from rest_framework.test import APITestCase
from django.urls import reverse_lazy

from ..models import StaffMember, ManageMember, SaleMember, SupportMember
from .utils import get_user_test, NeedToken

class TestUserViewset(APITestCase, NeedToken):

    def setUp(self) -> None:
        StaffMember.init_default_groups()
        return super().setUp()

    def do_as_response(self, do, as_class, args=[], kwargs={}) -> list:
        user_data = {
            'username': 'user_test',
            'password': 'password'
        }
        user_object = get_user_test(as_class, **user_data)
        user_tokens = self.get_user_token(**user_data)['access']
        result = do(token=user_tokens, *args, **kwargs)
        user_object.delete()
        return result
    
    def create_user(self, token: str|None = None, user_data: bool = True) -> list:
        status_codes = []
        for subclass in StaffMember.__subclasses__():
            create_link = reverse_lazy('authentication:user-specific-create', kwargs={'member_type': subclass.__name__.lower(),})
            response = self.client.post(
                path=create_link,
                data={
                    'username': f'username_test_{subclass.__name__.lower()}',
                    'email': 'username_test@epicevent.com',
                    'first_name': 'user',
                    'last_name': 'test',
                    'password': 'password'
                } if user_data else {},
                HTTP_AUTHORIZATION=f'Bearer {token}' if token is not None else None
            )
            status_codes.append(response.status_code)
            try:
                subclass.objects.get(username=f'username_test_{subclass.__name__.lower()}').delete()
            except subclass.DoesNotExist:
                pass
        return status_codes

    def list_users(self, token: str|None = None):
        status_codes = []
        list_link = reverse_lazy('authentication:user-list')
        response = self.client.get(
            path=list_link,
            HTTP_AUTHORIZATION=f'Bearer {token}' if token is not None else None
        )
        status_codes.append(response.status_code)
        return status_codes

    def retriev_user(self, token: str|None = None):
        status_codes = []
        for subclass in StaffMember.__subclasses__():
            test_user = subclass.objects.create(
                **{
                    'username': f'username_test_{subclass.__name__.lower()}',
                    'email': 'username_test@epicevent.com',
                    'first_name': 'user',
                    'last_name': 'test',
                    'password': 'password'
                }
            )
            detail_link = reverse_lazy('authentication:user-detail', kwargs={'pk': test_user.pk,})
            response = self.client.get(
                path=detail_link,
                HTTP_AUTHORIZATION=f'Bearer {token}' if token is not None else None
            )
            status_codes.append(response.status_code)
            test_user.delete()
        return status_codes

    def update_user(self, token: str|None = None, user_data: bool = True):
        status_codes = []
        for subclass in StaffMember.__subclasses__():
            test_user = subclass.objects.create(
                **{
                    'username': f'username_test_{subclass.__name__.lower()}',
                    'email': 'username_test@epicevent.com',
                    'first_name': 'user',
                    'last_name': 'test',
                    'password': 'password'
                }
            )
            detail_link = reverse_lazy('authentication:user-detail', kwargs={'pk': test_user.pk,})
            response = self.client.put(
                path=detail_link,
                data={
                    'username': f'username_test_{subclass.__name__.lower()}',
                    'email': 'username_test@epicevent.com',
                    'first_name': 'new_user',
                    'last_name': 'new_test',
                    'password': 'new_password'
                } if user_data else {},
                HTTP_AUTHORIZATION=f'Bearer {token}' if token is not None else None
            )
            status_codes.append(response.status_code)
            try:
                subclass.objects.get(username=f'username_test_{subclass.__name__.lower()}').delete()
            except subclass.DoesNotExist:
                pass
        return status_codes

    def partial_update_user(self, token: str|None = None, user_data: bool = True):
        status_codes = []
        for subclass in StaffMember.__subclasses__():
            test_user = subclass.objects.create(
                **{
                    'username': f'username_test_{subclass.__name__.lower()}',
                    'email': 'username_test@epicevent.com',
                    'first_name': 'user',
                    'last_name': 'test',
                    'password': 'password'
                }
            )
            detail_link = reverse_lazy('authentication:user-detail', kwargs={'pk': test_user.pk,})
            response = self.client.patch(
                path=detail_link,
                data={
                    'username': f'username_test_{subclass.__name__.lower()}',
                    'email': 'username_test@epicevent.com',
                    'first_name': 'new_user',
                    'last_name': 'new_test',
                    'password': 'new_password'
                } if user_data else {},
                HTTP_AUTHORIZATION=f'Bearer {token}' if token is not None else None
            )
            status_codes.append(response.status_code)
            try:
                subclass.objects.get(username=f'username_test_{subclass.__name__.lower()}').delete()
            except subclass.DoesNotExist:
                pass
        return status_codes

    def delete_user(self, token: str|None = None):
        status_codes = []
        for subclass in StaffMember.__subclasses__():
            test_user = subclass.objects.create(
                **{
                    'username': f'username_test_{subclass.__name__.lower()}',
                    'email': 'username_test@epicevent.com',
                    'first_name': 'user',
                    'last_name': 'test',
                    'password': 'password'
                }
            )
            detail_link = reverse_lazy('authentication:user-detail', kwargs={'pk': test_user.pk,})
            response = self.client.delete(
                path=detail_link,
                HTTP_AUTHORIZATION=f'Bearer {token}' if token is not None else None
            )
            status_codes.append(response.status_code)
            try:
                subclass.objects.get(username=f'username_test_{subclass.__name__.lower()}').delete()
            except subclass.DoesNotExist:
                pass
        return status_codes

    def test_create_success(self):
        #Create user as ManageMember should success
        status_codes = self.do_as_response(do=self.create_user, as_class=ManageMember)
        self.assertFalse(
            False in [
                status_code == 200 for status_code in status_codes
            ]
        )

    def test_create_error(self):
        #Try to create user without get log in should return 403
        status_codes = self.create_user()
        self.assertFalse(
            False in [
                status_code == 403 for status_code in status_codes
            ],
            'Unlog user shouldn\'t create user !'
        )
        
        #Try to create user as SaleMember should return 403
        status_codes = self.do_as_response(do=self.create_user, as_class=SaleMember)
        self.assertFalse(
            False in [
                status_code == 403 for status_code in status_codes
            ],
            'SaleMember user shouldn\'t create user !'
        )
        #Try to create user as SupportMember should return 403
        status_codes = self.do_as_response(do=self.create_user, as_class=SupportMember)
        self.assertFalse(
            False in [
                status_code == 403 for status_code in status_codes
            ],
            'SupportMember user shouldn\'t create user !'
        )
        #Try to create user with missing data should return 400
        status_codes = self.do_as_response(
            do=self.create_user,
            as_class=ManageMember,
            kwargs={'user_data': False}
        )
        self.assertFalse(
            False in [
                status_code == 400 for status_code in status_codes
            ],
            'Try to create user with missing data should return 400 !'
        )

    def test_list_success(self):
        #List users as ManageMember should success
        status_codes = self.do_as_response(do=self.list_users, as_class=ManageMember)
        self.assertFalse(
            False in [
                status_code == 200 for status_code in status_codes
            ]
        )

    def test_list_error(self):
        #Try to list users without get log in should return 403
        status_codes = self.list_users()
        self.assertFalse(
            False in [
                status_code == 403 for status_code in status_codes
            ],
            'Unlog user shouldn\'t list users !'
        )
        #Try to list users as SaleMember should return 403
        status_codes = self.do_as_response(do=self.list_users, as_class=SaleMember)
        self.assertFalse(
            False in [
                status_code == 403 for status_code in status_codes
            ],
            'SaleMember user shouldn\'t list users !'
        )
        #Try to list users as SupportMember should return 403
        status_codes = self.do_as_response(do=self.list_users, as_class=SaleMember)
        self.assertFalse(
            False in [
                status_code == 403 for status_code in status_codes
            ],
            'SupportMember user shouldn\'t list users !'
        )

    def test_retrieve_success(self):
        #Retrieve user as ManageMember should success
        status_codes = self.do_as_response(do=self.retriev_user, as_class=ManageMember)
        self.assertFalse(
            False in [
                status_code == 200 for status_code in status_codes
            ]
        )

    def test_retrieve_error(self):
        #Try to retrieve user without get log in should return 403
        status_codes = self.retriev_user()
        self.assertFalse(
            False in [
                status_code == 403 for status_code in status_codes
            ]
        )
        #Try to retrieve user as SaleMember should return 403
        status_codes = self.do_as_response(do=self.retriev_user, as_class=SaleMember)
        self.assertFalse(
            False in [
                status_code == 403 for status_code in status_codes
            ]
        )
        #Try to retrieve user as SupportMember should return 403
        status_codes = self.do_as_response(do=self.retriev_user, as_class=SupportMember)
        self.assertFalse(
            False in [
                status_code == 403 for status_code in status_codes
            ]
        )

    def test_update_success(self):
        #Update user as ManageMember should success
        status_codes = self.do_as_response(do=self.update_user, as_class=ManageMember)
        self.assertFalse(
            False in [
                status_code == 200 for status_code in status_codes
            ]
        )

    def test_update_error(self):
        #Try to update user without get log in should return 403
        status_codes = self.update_user()
        self.assertFalse(
            False in [
                status_code == 403 for status_code in status_codes
            ]
        )
        #Try to update another user as SaleMember should return 403
        status_codes = self.do_as_response(do=self.update_user, as_class=SaleMember)
        self.assertFalse(
            False in [
                status_code == 403 for status_code in status_codes
            ]
        )
        #Try to update another user as SupportMember should return 403
        status_codes = self.do_as_response(do=self.update_user, as_class=SupportMember)
        self.assertFalse(
            False in [
                status_code == 403 for status_code in status_codes
            ]
        )
        #Try to create user with missing data should return 400
        status_codes = self.do_as_response(
            do=self.update_user,
            as_class=SupportMember,
            kwargs={'user_data': False}
        )
        self.assertFalse(
            False in [
                status_code//100 != 2 for status_code in status_codes
            ]
        )

    def test_delete_error(self):
        #Try to delete user should return 403
        for subclass in StaffMember.__subclasses__():
            status_codes = self.do_as_response(do=self.delete_user, as_class=subclass)
            self.assertFalse(
                False in [
                    status_code == 403 for status_code in status_codes
                ]
            )
        status_codes = self.delete_user()
        self.assertFalse(
            False in [
                status_code == 403 for status_code in status_codes
            ]
        )
    
    def test_partial_update_error(self):
        #Try to partial user user should return 403
        for subclass in StaffMember.__subclasses__():
            status_codes = self.do_as_response(do=self.partial_update_user, as_class=subclass)
            self.assertFalse(
                False in [
                    status_code == 403 for status_code in status_codes
                ]
            )
        status_codes = self.delete_user()
        self.assertFalse(
            False in [
                status_code == 403 for status_code in status_codes
            ]
        )