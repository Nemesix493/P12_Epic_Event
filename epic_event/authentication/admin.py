from typing import Any, Optional
from django.contrib import admin
from django.http.request import HttpRequest


from .models import SaleMember, StaffMember, SupportMember, ManageMember


class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email']
    readonly_fields = ['is_staff', 'is_superuser', 'last_login', 'groups', 'user_permissions', 'date_joined', 'is_active']
    exclude = ['password']
    actions = ['deactivate']

    @admin.action(
        permissions=["change"],
        description="Set is_active fields to False"
    )
    def deactivate(modeladmin, request, queryset):
        queryset.update(is_active=False)

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return [field for field in self.readonly_fields if field != 'password']
        else:
            return self.readonly_fields
    
    def get_exclude(self, request: HttpRequest, obj=None) -> Any:
        if not obj:
            return []
        else:
            return self.exclude

@admin.register(SaleMember)
class SaleMemberAdmin(StaffMemberAdmin):
    pass

@admin.register(SupportMember)
class SupportMemberAdmin(StaffMemberAdmin):
    pass

@admin.register(ManageMember)
class ManageMemberAdmin(StaffMemberAdmin):
    pass