from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response
from rest_framework.decorators import action

from authentication.exceptions import AccessDenied
from authentication.models import SaleMember
from ..models import Prospect
from ..serializer import DetailProspectSerializer, ListProspectSerializer, WriteProspectSerializer
from ..permissions import ProspectPermission

class ProspectViewset(ModelViewSet):
    permission_classes = [ProspectPermission]
    queryset = Prospect.objects.all()
    filterset_fields = ListProspectSerializer.Meta.fields

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailProspectSerializer
        elif self.action == 'list':
            return ListProspectSerializer
        elif self.action == 'create' or self.action == 'update':
            return WriteProspectSerializer
    
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
    
    @action(detail=True, methods=['POST'], url_path='to-client', url_name='to-client')
    def to_client(self, request, *args, **kwargs):
        if isinstance(request.user.children, SaleMember):
            self.get_object().to_client(request.user.children)
            return Response(
                {'success': 'Success !'},
                200
            )
        return Response(
                {'error': 'You must be a salemember !'},
                403
            )