from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response
from rest_framework.decorators import action

from authentication.exceptions import BadRequest, NotFound
from authentication.models import SupportMember
from ..models import Event
from ..serializer import DetailEventSerializer, ListEventSerializer, WriteEventSerializer
from ..permissions import EventPermission

class EventViewset(ModelViewSet):
    permission_classes = [EventPermission]
    queryset = Event.objects.all()

    def get_support(self):
        support_pk = self.request.data.get('support_contact', None)
        if support_pk is None:
            raise BadRequest('Missing argument \'support_contact\' !')
        try:
            return SupportMember.objects.get(pk=support_pk)
        except SupportMember.DoesNotExist:
            raise NotFound('Not found \'support_contact\' no suport user with this ID !')

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'set_support':
            return DetailEventSerializer
        elif self.action == 'list':
            return ListEventSerializer
        elif self.action == 'create' or self.action == 'update':
            return WriteEventSerializer
    
    def destroy(self, request, *args, **kwargs):
        return Response(
            {'error': 'Destroy not available !'},
            403
        )
    
    def partial_update(self, request, *args, **kwargs):
        return Response(
            {'error': 'Partial update not available !'},
            403
        )
    
    @action(detail=True, methods=['POST'], url_path='set-support', url_name='set-support')
    def set_support(self, request, *args, **kwargs):
        event = self.get_object()
        event.support_contact = self.get_support()
        event.save()
        return Response(
            self.get_serializer_class()(instance=event).data
        )
