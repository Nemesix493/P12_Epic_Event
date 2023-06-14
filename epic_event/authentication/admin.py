from typing import Optional
from django.contrib import admin
from django.http.request import HttpRequest


from .models import SaleMember, StaffMember, SupportMember, ManageMember

class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email']
    readonly_fields = ['is_staff', 'is_superuser', 'last_login', 'groups', 'user_permissions', 'date_joined']
    exclude = ['password']

@admin.register(SaleMember)
class SaleMemberAdmin(StaffMemberAdmin):
    pass

@admin.register(SupportMember)
class SupportMemberAdmin(StaffMemberAdmin):
    pass

@admin.register(ManageMember)
class ManageMemberAdmin(StaffMemberAdmin):
    pass