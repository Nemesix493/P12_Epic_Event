from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response
from rest_framework.decorators import action

from authentication.exceptions import AccessDenied
from authentication.models import SaleMember
from ..models import Client
from ..serializer import DetailClientSerializer, ListClientSerializer, WriteClientSerializer
from ..permissions import ClientPermission

class ClientViewset(ModelViewSet):
    permission_classes = [ClientPermission]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailClientSerializer
        elif self.action == 'list':
            return ListClientSerializer
        elif self.action == 'create' or self.action == 'update':
            return WriteClientSerializer
    
    def get_queryset(self):
        return Client.objects.all()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        user_children = request.user.children
        if isinstance(user_children, SaleMember):
            serializer.save_with_sale_contact(sale_contact=user_children)
            return Response(
                serializer.data,
                201
            )
        return Response(
            {'error': 'You must be a salemember !'},
            403
        )
    
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
