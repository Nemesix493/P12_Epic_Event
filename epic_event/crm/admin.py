from typing import Any
from django.contrib import admin

# Register your models here.
from .models import Prospect, Client, Contract
from authentication.models import SaleMember

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name','first_name', 'last_name']

@admin.register(Prospect)
class ProspectAdmin(CompanyAdmin):
    actions = ['prospect_to_client']
    @admin.action(
        permissions=["change"],
        description="Update prospect to client"
    )
    def prospect_to_client(modeladmin, request, queryset):
        for prospect in queryset:
            prospect.to_client()


@admin.register(Client)
class ClientAdmin(CompanyAdmin):
    readonly_fields = ['sale_contact']

    def save_model(self, request: Any, obj: Client, form: Any, change: Any) -> None:
        if not change:
            obj.sale_contact = request.user.children
        return super().save_model(request, obj, form, change)


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['client_company_name', 'amount', 'status', 'payment_due']
    readonly_fields = ['date_created', 'date_updated']
