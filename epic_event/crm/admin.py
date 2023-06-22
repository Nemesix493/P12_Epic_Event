from typing import Any, Optional
from django.contrib import admin
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.models import Permission

# Register your models here.
from .models import Prospect, Client, Contract, Event
from authentication.models import SaleMember, SupportMember
from .forms import SetSupportForm

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

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['client_company_name', 'attendees', 'event_date']
    readonly_fields = ['date_created', 'date_updated', 'support_contact']
    change_list_template = 'go_to_set_support.html'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('set-support/', self.admin_site.admin_view(self.set_support), name='set_support'),
            path('change-support/', self.admin_site.admin_view(self.change_support), name='change_support')
        ]
        return custom_urls + urls

    def set_support(self, request):
        return self.support_view(
            request=request,
            events=Event.objects.all().filter(support_contact=None),
            supportmembers=SupportMember.objects.all(),
            action='admin:set_support'
        )   
    
    def change_support(self, request):
        return self.support_view(
            request=request,
            events=Event.objects.all().exclude(support_contact=None),
            supportmembers=SupportMember.objects.all(),
            action='admin:change_support'
        )

    def support_view(self, request, events, supportmembers, action):
        permission_natural_key = Permission.objects.get(codename=f'set_support_event').natural_key()
        if not request.user.has_perm(f'{permission_natural_key[1]}.{permission_natural_key[0]}'):
            return redirect('admin:crm_event_changelist')
        if request.method == 'POST':
            form = SetSupportForm(
                events,
                supportmembers,
                request.POST
            )
            if form.is_valid():
                event = events.get(pk=int(form.cleaned_data['event']))
                event.support_contact = supportmembers.get(pk=int(form.cleaned_data['support']))
                event.save()
                return self.response_post_save_change(request, event)
        else:
            form = SetSupportForm(
                events=events,
                supports=supportmembers
            )
        context = self.admin_site.each_context(request)
        context['form'] = form
        context['action'] = action
        return render(request, 'set_support.html', context)