import datetime

import pytz
from django.urls import reverse_lazy

from authentication.models import SaleMember, SupportMember, ManageMember, StaffMember
from ..models import Contract, Client
from .utils import TestViewsets

class TestContractViewset(TestViewsets):

    client_exemple_data = {
        'first_name': 'client_first_name',
        'last_name': 'client_last_name',
        'email': 'client_exemple@oc.fr',
        'phone': '+33257624278',
        'mobile': '+33657624278',
        'company_name': 'client_company_name',
    }

    contract_exemple_data = {
        'status': False,
        'amount': 1000,
        'payment_due': datetime.datetime.now(tz=pytz.UTC) + datetime.timedelta(days=5)
    }

    def setUp(self) -> None:
        super().setUp()
        self.sale_contact = self.get_user_test(SaleMember, 'client_user_creator', 'password')
        self.client_object = Client.objects.create(
            **{
                **self.client_exemple_data,
                'sale_contact': self.sale_contact
            }
        )

    def get_test_contract(self):
        return Contract.objects.create(
            **{
                **self.contract_exemple_data,
                'client': self.client_object
            }
        )

    def get_link(self, link_type: str, args=[], kwargs={}) -> str:
        if link_type == 'list':
            return reverse_lazy('crm:contract-list')
        elif link_type == 'detail':
            return reverse_lazy('crm:contract-detail', args=args, kwargs=kwargs)
        else:
            raise AttributeError()
    
    def test_list_success(self):
        #list the contracts as salemember or supportmember or managemember should success
        for member_type in [ManageMember, SupportMember, SaleMember]:
            response = self.do_as_response(
                self.list,
                member_type,
            )
            self.assertEqual(200, response.status_code)
    
    def test_list_error(self):
        #list the contracts without loged in should result 403
        response = self.list()
        self.assertEqual(403, response.status_code)
    
    def test_retrieve_success(self):
        #retriev a contract as salemember or supportmember or managemember should success
        test_contract = self.get_test_contract()
        for member_type in [ManageMember, SupportMember, SaleMember]:
            response = self.do_as_response(
                self.retrieve,
                member_type,
                kwargs={
                    'pk': test_contract.pk
                }
            )
            self.assertEqual(200, response.status_code)
    
    def test_retrieve_error(self):
        #try retrieve a contract without loged in should result 403
        test_contract = self.get_test_contract()
        response = self.retrieve(pk=test_contract.pk)
        self.assertEqual(403, response.status_code)
    
    def test_create_success(self):
        #create a contract as salemember should success
        response = self.do_as_response(
            self.create,
            SaleMember,
            kwargs={
                'object_data':{
                    **self.contract_exemple_data,
                    'client': self.client_object.pk
                }
            }
        )
        self.assertEqual(201, response.status_code)
    
    def test_create_error(self):
        #try to create a contract as managemember or supportmember should result 403
        for member_type in [ManageMember, SupportMember]:
            response = self.do_as_response(
                self.create,
                member_type,
                kwargs={
                    'object_data':{
                        **self.contract_exemple_data,
                        'client': self.client_object.pk
                    }
                }
            )
            self.assertEqual(403, response.status_code)
        #try to create a contract without loged in should result 403
        response = self.create(
            object_data={
                **self.contract_exemple_data,
                'client': self.client_object.pk
            }
        )
        self.assertEqual(403, response.status_code)
    
    def test_update_success(self):
        #update a contract as salemember should success
        test_contract = self.get_test_contract()
        response = self.do_as_response(
            self.update,
            SaleMember,
            kwargs={
                'pk': test_contract.pk,
                'object_data': {
                    **{
                        key: val
                        if key != 'amount' else val/2
                        for key, val in self.contract_exemple_data.items()
                    },
                    'client': self.client_object.pk
                }
            }
        )
        self.assertEqual(200, response.status_code)
    
    def test_update_error(self):
        test_contract = self.get_test_contract()
        #try to update a contract as managemember or supportmember should result 403
        for member_type in [ManageMember, SupportMember]:
            response = self.do_as_response(
                self.update,
                member_type,
                kwargs={
                    'pk': test_contract.pk,
                    'object_data': {
                        **{
                            key: val
                            if key != 'amount' else val/2
                            for key, val in self.contract_exemple_data.items()
                        },
                        'client': self.client_object.pk
                    }
                }
            )
            self.assertEqual(403, response.status_code)
        #try to update a contract without loged in should result 403
        response = self.update(
            pk=test_contract.pk,
            object_data={
                **self.contract_exemple_data,
                'client': self.client_object.pk
            }
        )
        self.assertEqual(403, response.status_code)
    
    def test_destroy_error(self):
        test_contract = self.get_test_contract()
        #try to delete a contract should result 403
        for member_type in [ManageMember, SupportMember, SaleMember]:
            response = self.do_as_response(
                self.destroy,
                member_type,
                kwargs={
                    'pk': test_contract.pk
                }
            )
            self.assertEqual(403, response.status_code)
        response = self.destroy(pk=test_contract.pk)
        self.assertEqual(403, response.status_code)
