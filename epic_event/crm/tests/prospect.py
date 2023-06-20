from django.urls import reverse_lazy

from authentication.models import SaleMember, SupportMember, ManageMember, StaffMember
from ..models import Prospect
from .utils import TestViewsets

class TestProspectViewset(TestViewsets):

    prospect_exemple_data = {
        'first_name': 'prospect_first_name',
        'last_name': 'prospect_last_name',
        'email': 'prospect_exemple@oc.fr',
        'phone': '+33257624278',
        'mobile': '+33657624278',
        'company_name': 'porspect_company_name',
    }

    def get_link(self, link_type: str, args=[], kwargs={}) -> str:
        if link_type == 'list':
            return reverse_lazy('crm:prospect-list')
        elif link_type == 'detail':
            return reverse_lazy('crm:prospect-detail', args=args, kwargs=kwargs)
        else:
            raise AttributeError()
    
    def to_client(self, token: str|None = None, pk=None):
        to_client_link = reverse_lazy('crm:prospect-to-client', kwargs={'pk': pk,})
        response = self.client.post(
                path=to_client_link,
                HTTP_AUTHORIZATION=f'Bearer {token}' if token is not None else None
            )
        return response

    def test_list_success(self):
        #list the prospect as salemember should success
        response = self.do_as_response(
            self.list,
            SaleMember,
        )
        self.assertEqual(200, response.status_code)
    
    def test_list_error(self):
        #list the prospect as supportmember or managemember should result 403
        for member_type in [ManageMember, SupportMember]:
            response = self.do_as_response(
                self.list,
                member_type,
            )
            self.assertEqual(403, response.status_code, f'{response.json()}')
        #list the prospect without loged in should result 403
        response = self.list()
        self.assertEqual(403, response.status_code, 'Unloged !!')
    
    def test_retrieve_success(self):
        #retriev a prospect as salemember should success
        prospect_test = Prospect.objects.create(**self.prospect_exemple_data)
        response = self.do_as_response(
            self.retriev,
            SaleMember,
            kwargs={
                'pk': prospect_test.pk
            }
        )
        self.assertEqual(200, response.status_code, f'{response.json()}')
    
    def test_retriev_error(self):
        #retriev a prospect as supportmember or managemember should result 403
        prospect_test = Prospect.objects.create(**self.prospect_exemple_data)
        for member_type in [ManageMember, SupportMember]:
            response = self.do_as_response(
                self.retriev,
                member_type,
                kwargs={
                    'pk': prospect_test.pk
                }
            )
            self.assertEqual(403, response.status_code)
        #retriev a prospect without loged in should result 403
        response = self.retriev(pk=prospect_test.pk)
        self.assertEqual(403, response.status_code, 'Unloged !!')
    
    def test_create_success(self):
        #create a prospect as salemember should success
        response = self.do_as_response(
            self.create,
            SaleMember,
            kwargs={
                'prospect_data': self.prospect_exemple_data
            }
        )
        self.assertEqual(201, response.status_code, str(response.json()))
    
    def test_create_error(self):
        #create a prospect as supportmember or managemember should result 403
        for member_type in [ManageMember, SupportMember]:
            response = self.do_as_response(
                self.create,
                member_type,
                kwargs={
                    'prospect_data': self.prospect_exemple_data
                }
            )
            self.assertEqual(403, response.status_code)
        #create a prospect without loged in should result 403
        response = self.create(prospect_data=self.prospect_exemple_data)
        self.assertEqual(403, response.status_code)
    
    def test_update_success(self):
        prospect_test = Prospect.objects.create(**self.prospect_exemple_data)
        #update a prospect as salemember should success
        response = self.do_as_response(
            self.update,
            SaleMember,
            kwargs={
                'pk':prospect_test.pk,
                'prospect_data': {
                    key: val
                    if key != 'first_name' else f'new_{val}'
                    for key, val in self.prospect_exemple_data.items()
                }
            }
        )
        self.assertEqual(200, response.status_code, str(response.json()))
    
    def test_update_error(self):
        prospect_test = Prospect.objects.create(**self.prospect_exemple_data)
        #update a prospect as supportmember or managemember should result 403
        for member_type in [ManageMember, SupportMember]:
            response = self.do_as_response(
                self.update,
                member_type,
                kwargs={
                    'pk':prospect_test.pk,
                    'prospect_data': {
                        key: val
                        if key != 'first_name' else f'new_{val}'
                        for key, val in self.prospect_exemple_data.items()
                    }
                }
            )
            self.assertEqual(403, response.status_code)
        #update a prospect without loged in should result 403
        response = self.update(pk=prospect_test.pk, prospect_data=self.prospect_exemple_data)
        self.assertEqual(403, response.status_code, 'Unloged !!')

    def test_delete_error(self):
        #no one can delete a prospect
        prospect_test = Prospect.objects.create(**self.prospect_exemple_data)
        for member_type in [SaleMember, ManageMember, SupportMember]:
            response = self.do_as_response(
                self.delete,
                member_type,
                kwargs={
                    'pk':prospect_test.pk,
                }
            )
            self.assertEqual(403, response.status_code)
        response = self.delete(pk=prospect_test.pk)
        self.assertEqual(403, response.status_code)

    def test_to_client_success(self):
        prospect_test = Prospect.objects.create(**self.prospect_exemple_data)
        #update a prospect to client as salemember should success
        response = self.do_as_response(
            self.to_client,
            SaleMember,
            kwargs={
                'pk':prospect_test.pk,
            }
        )
        self.assertEqual(200, response.status_code)

    def test_to_client_error(self):
        prospect_test = Prospect.objects.create(**self.prospect_exemple_data)
        #update a prospect to client as supportmember or managemember should result 403
        for member_type in [ManageMember, SupportMember]:
            response = self.do_as_response(
                self.to_client,
                member_type,
                kwargs={
                    'pk':prospect_test.pk,
                }
            )
            self.assertEqual(403, response.status_code)
        #update a prospect to client without loged in should result 403
        response = self.to_client(pk=prospect_test.pk)
        self.assertEqual(403, response.status_code, 'Unloged !!')
