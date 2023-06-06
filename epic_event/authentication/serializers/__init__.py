from .staffmember import DetailsStaffMemberSerializer, ListStaffMemberSerializer
from .salemember import DetailsSaleMemberSerializer, WriteSaleMemberSerializer
from .supportmember import DetailsSupportMemberSerializer, WriteSupportMemberSerializer
from .managemember import DetailsManageMemberSerializer, WriteManageMemberSerializer
from ..models import ManageMember, SaleMember, SupportMember


DetailsStaffMemberSerializer.serializer_type = [
    (ManageMember, DetailsManageMemberSerializer),
    (SupportMember, DetailsSupportMemberSerializer),
    (SaleMember, DetailsSaleMemberSerializer)
]
