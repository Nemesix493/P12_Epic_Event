from ..models import Client
from .basepermission import CustomBasePermission

class ClientPermission(CustomBasePermission):
    model = Client