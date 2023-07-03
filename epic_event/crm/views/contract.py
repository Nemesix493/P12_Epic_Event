from rest_framework.viewsets import ModelViewSet
from rest_framework.views import Response

from ..models import Contract
from ..serializer import DetailContractSerializer, ListContractSerializer, WriteContractSerializer
from ..permissions import ContractPermission

class ContractViewset(ModelViewSet):
    permission_classes = [ContractPermission]
    queryset = Contract.objects.all()
    filterset_fields = ListContractSerializer.Meta.fields

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailContractSerializer
        elif self.action == 'list':
            return ListContractSerializer
        elif self.action == 'create' or self.action == 'update':
            return WriteContractSerializer
    
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
