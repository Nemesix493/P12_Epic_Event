from django.urls import reverse_lazy

from authentication.models import SaleMember, SupportMember, ManageMember, StaffMember
from ..models import Client
from .utils import TestViewsets

class TestClientViewset(TestViewsets):
    client_exemple_data = {
        'first_name': 'client_first_name',
        'last_name': 'client_last_name',
        'email': 'client_exemple@oc.fr',
        'phone': '+33257624278',
        'mobile': '+33657624278',
        'company_name': 'client_company_name',
    }

    def get_link(self, link_type: str, args=[], kwargs={}) -> str:
        if link_type == 'list':
            return reverse_lazy('crm:client-list')
        elif link_type == 'detail':
            return reverse_lazy('crm:client-detail', args=args, kwargs=kwargs)
        else:
            raise AttributeError()
    
    def test_list_success(self):
        #list the clients as salemember or supportmember should success
        for member_type in [SaleMember, SupportMember]:
            response = self.do_as_response(
                self.list,
                member_type,
            )
            self.assertEqual(200, response.status_code)
    
    def test_list_error(self):
        #try to list the clients as managemember should result 403
        response = self.do_as_response(
            self.list,
            ManageMember,
        )
        self.assertEqual(403, response.status_code)
        #try to list the clients without loged in should result 403
        response = self.list()
        self.assertEqual(403, response.status_code)
    
    def test_retrieve_success(self):
        #retrieve a client as salemember or supportmember should success
        client_test = Client.objects.create(
            **{
                **self.client_exemple_data,
                'sale_contact': SaleMember.objects.create(
                    username='client_test_retrieve',
                    password='password'
                )
            }
        )
        for member_type in [SaleMember, SupportMember]:
            response = self.do_as_response(
                self.retrieve,
                member_type,
                kwargs={
                    'pk':client_test.pk
                }
            )
            self.assertEqual(200, response.status_code)
    
    def test_retrieve_error(self):
        client_test = Client.objects.create(
            **{
                **self.client_exemple_data,
                'sale_contact': SaleMember.objects.create(
                    username='client_test_retrieve',
                    password='password'
                )
            }
        )
        #try to retrieve a client as managemember should result 403
        response = self.do_as_response(
            self.retrieve,
            ManageMember,
            kwargs={
                'pk':client_test.pk
            }

        )
        self.assertEqual(403, response.status_code)
        #try to retrieve a client without loged in should result 403
        response = self.retrieve(pk=client_test.pk)
        self.assertEqual(403, response.status_code)
    
    def test_create_success(self):
        #create a client as salemember should success
        response = self.do_as_response(
            self.create,
            SaleMember,
            kwargs={
                'object_data': self.client_exemple_data
            }

        )
        self.assertEqual(201, response.status_code)
    
    def test_create_error(self):
        #try to create a client as managemember or supportmember should result 403
        for member_type in [SupportMember, ManageMember]:
            response = self.do_as_response(
                self.create,
                member_type,
                kwargs={
                    'object_data': self.client_exemple_data
                }
            )
            self.assertEqual(403, response.status_code)
        #try to create a client without loged in should result 403
        response = self.create(object_data=self.client_exemple_data)
        self.assertEqual(403, response.status_code)

    def test_update_success(self):
        client_test = Client.objects.create(
            **{
                **self.client_exemple_data,
                'sale_contact': SaleMember.objects.create(
                    username='client_test_update',
                    password='password'
                )
            }
        )
        #update a client as salemember should success
        response = self.do_as_response(
            self.update,
            SaleMember,
            kwargs={
                'object_data': {
                    key: val
                    if key != 'first_name' else f'new_{val}'
                    for key, val in self.client_exemple_data.items()
                },
                'pk': client_test.pk
            }
        )
        self.assertEqual(200, response.status_code)
    
    def test_update_error(self):
        client_test = Client.objects.create(
            **{
                **self.client_exemple_data,
                'sale_contact': SaleMember.objects.create(
                    username='client_test_update',
                    password='password'
                )
            }
        )
        #try to update a client as managemember or supportmember should result 403
        for member_type in [ManageMember, SupportMember]:
            response = self.do_as_response(
                self.update,
                member_type,
                kwargs={
                    'object_data': {
                        key: val
                        if key != 'first_name' else f'new_{val}'
                        for key, val in self.client_exemple_data.items()
                    },
                    'pk': client_test.pk
                }
            )
            self.assertEqual(403, response.status_code)
        #try to update a client without loged in should result 403
        response = self.update(
            object_data={
                key: val
                if key != 'first_name' else f'new_{val}'
                for key, val in self.client_exemple_data.items()
            },
            pk=client_test.pk
        )
        self.assertEqual(403, response.status_code)
    
    def test_destroy_error(self):
        client_test = Client.objects.create(
            **{
                **self.client_exemple_data,
                'sale_contact': SaleMember.objects.create(
                    username='client_test_delete',
                    password='password'
                )
            }
        )
        #try to delete a client should result 403
        for member_type in [ManageMember, SupportMember, SaleMember]:
            response = self.do_as_response(
                self.destroy,
                member_type,
                kwargs={
                    'pk': client_test.pk
                }
            )
            self.assertEqual(403, response.status_code)
        response = self.destroy(
            pk=client_test.pk
        )
        self.assertEqual(403, response.status_code)
    