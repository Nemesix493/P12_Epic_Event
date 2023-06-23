from ..models import Contract
from .basepermission import CustomBasePermission

class ContractPermission(CustomBasePermission):
    model = Contract