import datetime

import pytz
from django.urls import reverse_lazy

from authentication.models import SaleMember, SupportMember, ManageMember, StaffMember
from ..models import Event, Client, Contract
from .utils import TestViewsets

class TestEventViewset(TestViewsets):

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

    event_exemple_data = {
        'event_date': datetime.datetime.now(tz=pytz.UTC) + datetime.timedelta(days=15),
        'notes': 'Some notes',
        'attendees': 50
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
        self.contract = Contract.objects.create(
            **{
                **self.contract_exemple_data,
                'client': self.client_object
            }
        )
    
    def get_test_event(self):
        return Event.objects.create(
            **{
                **self.event_exemple_data,
                'event_status': self.contract
            }
        )

    def get_link(self, link_type: str, args=[], kwargs={}) -> str:
        if link_type == 'list':
            return reverse_lazy('crm:event-list')
        elif link_type == 'detail':
            return reverse_lazy('crm:event-detail', args=args, kwargs=kwargs)
        else:
            raise AttributeError()
    
    def set_support(self, event_pk: int, support_pk: int, token: str | None = None):
        set_support_link = reverse_lazy('crm:event-set-support', kwargs={'pk': event_pk})
        response = self.client.post(
                path=set_support_link,
                data={
                    'support_contact': support_pk
                },
                HTTP_AUTHORIZATION=f'Bearer {token}' if token is not None else None
            )
        return response

    def test_list_success(self):
        #list the events as salemember or supportmember or managemember should success
        for member_type in [ManageMember, SupportMember, SaleMember]:
            response = self.do_as_response(
                self.list,
                member_type,
            )
            self.assertEqual(200, response.status_code)
    
    def test_list_error(self):
        #try to list the events without loged in should result 403
        response = self.list()
        self.assertEqual(403, response.status_code)
    
    def test_retrieve_success(self):
        test_event = self.get_test_event()
        #retrieve an event as salemember or supportmember or managemember should success
        for member_type in [ManageMember, SupportMember, SaleMember]:
            response = self.do_as_response(
                self.retrieve,
                member_type,
                kwargs={
                    'pk': test_event.pk
                }
            )
            self.assertEqual(200, response.status_code)
    
    def test_retrieve_error(self):
        test_event = self.get_test_event()
        #try to retrieve an event without loged in should result 403
        response = self.retrieve(pk=test_event.pk)
        self.assertEqual(403, response.status_code)

    def test_create_success(self):
        #create an event as salemember should success
        response = self.create(
            token=self.get_user_token(
                username='client_user_creator',
                password='password'
            )['access'],
            object_data={
                **self.event_exemple_data,
                'event_status': self.contract.pk
            }
        )
        self.assertEqual(201, response.status_code, str(response.json()))
    
    def test_create_error(self):
        #try to create an event as supportmember or managemember should result 403
        for member_type in [ManageMember, SupportMember]:
            response = self.do_as_response(
                self.create,
                member_type,
                kwargs={
                    'object_data': {
                        **self.event_exemple_data,
                        'event_status': self.contract.pk
                    }
                }
            )
            self.assertEqual(403, response.status_code)
        #try to create an event without loged in should result 403
        response = self.create(
            object_data={
                **self.event_exemple_data,
                'event_status': self.contract.pk
            }
        )
        self.assertEqual(403, response.status_code)
    
    def test_update_success(self):
        test_event = self.get_test_event()
        support_contact = self.get_user_test(SupportMember, username='support_contact', password='password')
        test_event.support_contact = support_contact
        test_event.save()
        #update an event as supportmember linked to the event should success
        response = self.update(
            token=self.get_user_token(
                username='support_contact',
                password='password'
            )['access'],
            pk=test_event.pk,
            object_data={
                **{
                    key: val
                    if key != 'attendees' else 45
                    for key, val in self.event_exemple_data.items()
                },
                'event_status': self.contract.pk
            }
        )
        self.assertEqual(200, response.status_code, str(response.json()))
    
    def test_update_error(self):
        test_event = self.get_test_event()
        support_contact = self.get_user_test(SupportMember, username='support_contact', password='password')
        test_event.support_contact = support_contact
        test_event.save()
        #try to update an event as salemember or managemember should result 403
        #try to update an event as supportmember not linked to the event should result 403
        for member_type in [ManageMember, SupportMember, SaleMember]:
            response = self.do_as_response(
                self.update,
                member_type,
                kwargs={
                    'pk': test_event.pk,
                    'object_data': {
                        **{
                            key: val
                            if key != 'attendees' else 45
                            for key, val in self.event_exemple_data.items()
                        },
                        'event_status': self.contract.pk
                    }
                }
            )
            self.assertEqual(403, response.status_code)
        #try to update an event without loged in should result 403
        response = self.update(
                pk=test_event.pk,
                object_data={
                    **{
                        key: val
                        if key != 'attendees' else 45
                        for key, val in self.event_exemple_data.items()
                    },
                    'event_status': self.contract.pk
                }
        )
        self.assertEqual(403, response.status_code)
    
    def test_destroy_error(self):
        test_event = self.get_test_event()
        #try to delete an event should result 403
        for member_type in [ManageMember, SupportMember, SaleMember]:
            response = self.do_as_response(
                self.destroy,
                member_type,
                kwargs={
                    'pk': test_event.pk
                }
            )
            self.assertEqual(403, response.status_code)
        response = self.destroy(pk=test_event.pk)
        self.assertEqual(403, response.status_code)
    
    def test_set_support_success(self):
        test_event = self.get_test_event()
        support_contact = self.get_user_test(SupportMember, username='support_contact', password='password')
        #set_support to an event as managemember should success
        response = self.do_as_response(
            self.set_support,
            ManageMember,
            kwargs={
                'event_pk': test_event.pk,
                'support_pk': support_contact.pk
            }
        )
        self.assertEqual(200, response.status_code)
    
    def test_set_support_error(self):
        test_event = self.get_test_event()
        support_contact = self.get_user_test(SupportMember, username='support_contact', password='password')
        #try to set_support to an event as salemember or supportmember should result 403
        for member_type in [SupportMember, SaleMember]:
            response = self.do_as_response(
                self.set_support,
                member_type,
                kwargs={
                    'event_pk': test_event.pk,
                    'support_pk': support_contact.pk
                }
            )
            self.assertEqual(403, response.status_code)
        #try to set_support to an event without loged in should result 403
        response = self.set_support(
                event_pk=test_event.pk,
                support_pk=support_contact.pk
        )
        self.assertEqual(403, response.status_code)
