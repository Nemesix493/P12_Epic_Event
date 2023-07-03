from rest_framework.test import APITestCase
from django.urls import reverse_lazy

from ..models import StaffMember
from .utils import UserTokenMixin


class TestTokenObtainPairView(APITestCase, UserTokenMixin):
    def setUp(self) -> None:
        self.token_obtain_pair_link = reverse_lazy('authentication:token_obtain_pair')
        return super().setUp()
    
    def test_token_obtain_pair_success(self):
        user_test = {
            'username': 'user_test',
            'password': 'password'
        }
        self.get_user_test(StaffMember, **user_test)
        response = self.client.post(
            path=self.token_obtain_pair_link,
            data=user_test
        )
        self.assertEqual(response.status_code, 200)
    
    def test_token_obtain_pair_error(self):
        user_test = {
            'username': 'user_test',
            'password': 'password'
        }
        self.get_user_test(StaffMember, **user_test)
        #On wrong password request should return status 401
        response = self.client.post(
            path=self.token_obtain_pair_link,
            data={
                'username': 'user.test',
                'password': 'wrong_password_test'
            }
        )
        self.assertEqual(response.status_code, 401)
        #On wrong username request should return status 401
        response = self.client.post(
            path=self.token_obtain_pair_link,
            data={
                'username': 'wrong_user.test',
                'password': 'password_test'
            }
        )
        self.assertEqual(response.status_code, 401)