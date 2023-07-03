from typing import Any, Mapping, Optional, Type, Union
from django import forms
from django.forms.utils import ErrorList

class SetSupportForm(forms.Form):
    event = forms.ChoiceField()
    support = forms.ChoiceField()

    def __init__(self, events, supports, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.events = events
        self.supports = supports
        self.fields['event'].choices = self.events_to_choices(events)
        self.fields['support'].choices = self.supports_to_choices(supports)
    
    def events_to_choices(self, events) -> list[tuple]:
        return [
            (None, 15 * '-'),
            *[
                (event.pk, f'{event.client_company_name}: {event.event_date}')
                for event in events
            ]
        ]
    
    def supports_to_choices(self, supports) -> list[tuple]:
        return [
            (None, 15 * '-'),
            *[
                (supportmember.pk, f'{supportmember.first_name} {supportmember.last_name} : {supportmember.username}')
                for supportmember in supports
            ]
        ]
