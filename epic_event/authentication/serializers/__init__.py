from .staffmember import DetailsStaffMemberSerializer, ListStaffMemberSerializer
from .salemember import DetailsSaleMemberSerializer, WriteSaleMemberSerializer
from .supportmember import DetailsSupportMemberSerializer, WriteSupportMemberSerializer
from .managemember import DetailsManageMemberSerializer, WriteManageMemberSerializer
from ..models import ManageMember, SaleMember, SupportMember


DetailsStaffMemberSerializer.details_serializer_type = [
    (ManageMember, DetailsManageMemberSerializer),
    (SupportMember, DetailsSupportMemberSerializer),
    (SaleMember, DetailsSaleMemberSerializer)
]

WRITE_SERIALIZER_CLASS = [
    (ManageMember, WriteManageMemberSerializer),
    (SupportMember, WriteSupportMemberSerializer),
    (SaleMember, WriteSaleMemberSerializer)
]

