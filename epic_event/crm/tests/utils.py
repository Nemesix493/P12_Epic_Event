from abc import ABC, abstractmethod

from django.test import TestCase

from authentication.tests.utils import UserTokenMixin, DataBaseInitMixin

class TestViewsets(TestCase, UserTokenMixin, DataBaseInitMixin, ABC):

    def setUp(self) -> None:
        self.init_db()
        return super().setUp()
    
    @abstractmethod
    def get_link(self, link_type: str, args=[], kwargs={}) -> str:
        pass
    
    def list(self, token: str|None = None):
        response = self.client.get(
                path=self.get_link(link_type='list'),
                HTTP_AUTHORIZATION=f'Bearer {token}' if token is not None else None
            )
        return response

    def retriev(self, token: str|None = None, pk=None):
        response = self.client.get(
                path=self.get_link(link_type='detail', kwargs={'pk': pk,}),
                HTTP_AUTHORIZATION=f'Bearer {token}' if token is not None else None
            )
        return response

    def create(self, token: str|None = None, prospect_data: dict| None = None):
        response = self.client.post(
                path=self.get_link(link_type='list'),
                data= prospect_data if prospect_data else {},
                HTTP_AUTHORIZATION=f'Bearer {token}' if token is not None else None
            )
        return response

    def update(self, token: str|None = None, pk=None, prospect_data: dict| None = None):
        response = self.client.put(
                path=self.get_link(link_type='detail', kwargs={'pk': pk,}),
                data= prospect_data if prospect_data else {},
                HTTP_AUTHORIZATION=f'Bearer {token}' if token is not None else None,
                content_type='application/json'
            )
        return response

    def delete(self, token: str|None = None, pk=None):
        response = self.client.delete(
                path=self.get_link(link_type='detail', kwargs={'pk': pk,}),
                HTTP_AUTHORIZATION=f'Bearer {token}' if token is not None else None
            )
        return response