from rest_framework.exceptions import APIException
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.views import Response

from ..models import StaffMember, SupportMember, SaleMember, ManageMember
from ..permisssions.user import UserPermission
from ..serializers import ListStaffMemberSerializer, DetailsStaffMemberSerializer, WRITE_SERIALIZER_CLASS
from ..exceptions import BadRequest, NotFound


class UserViewset(ModelViewSet):
    permission_classes = [UserPermission]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            if self.action == 'list':
                return ListStaffMemberSerializer
            elif self.action == 'retrieve':
                return DetailsStaffMemberSerializer
        elif self.action == 'specific_create':
            for model_class, serializer_class in WRITE_SERIALIZER_CLASS:
                if self.kwargs.get('member_type') == model_class.__name__.lower():
                    return serializer_class
            raise BadRequest('member_type not valid !', request=self.request)
        elif self.request.method != 'GET':
            for model_class, serializer_class in WRITE_SERIALIZER_CLASS:
                if isinstance(self.get_object().children, model_class):
                    return serializer_class
            raise BadRequest('member_type not valid !', request=self.request)
        raise APIException('Internal error !')

    def get_object(self):
        try:
            obj = StaffMember.objects.get(pk=self.kwargs.get('pk'))
        except StaffMember.DoesNotExist:
            raise NotFound('Member not found !', request=self.request)
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        return StaffMember.objects.all()
    
    @action(detail=False, methods=['POST'], url_path=r'create/(?P<member_type>[a-z]+)', url_name='specific-create')
    def specific_create(self, request, member_type):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(str(serializer.error_messages), request=self.request)
        user = serializer.save()
        return Response(DetailsStaffMemberSerializer(instance=user).data)
    
    def create(self, request, *args, **kwargs):
        return Response(
            {'error': 'To create a user you must use create endpoint with '},
            403
        )
    
    def destroy(self, request, *args, **kwargs):
        return Response(
            {'error': 'Deletion not available !'},
            403
        )
    
    def partial_update(self, request, *args, **kwargs):
        return Response(
            {'error': 'Partial update not available !'},
            403
        )