import itertools
from typing import Any

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group


class StaffMember(AbstractUser):
    """Abstract like class"""
    is_staff = models.BooleanField(default=True)
    default_groups_name = []

    def add_default_groups(self):
        for group_name in self.default_groups_name:
            group = Group.objects.get(name=f'{group_name.capitalize()} Group')
            if group not in self.groups.all():
                self.groups.add(group)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            super(StaffMember, self).save(*args, **kwargs)
            self.add_default_groups()
        else:
            super(StaffMember, self).save(*args, **kwargs)

    @property
    def children(self):
        children = [self.__getattribute__(subclass.__name__.lower()) for subclass in self.__class__.__subclasses__() if hasattr(self, subclass.__name__.lower())]
        if len(children) == 0:
            raise AttributeError('Should have 1 children')
        elif len(children) != 1:
            raise TypeError(f'Should have 1 children not ({len(children)})!')
        
        return children[0]
    
    @classmethod
    def link_subclasses(cls) -> None:
        for subclass in cls.__subclasses__():
            subclass.parent = models.OneToOneField(cls, parent_link=True, on_delete=models.CASCADE, primary_key=True, related_name=subclass.__name__.lower())
    
    @classmethod
    def init_default_groups(cls) -> None:
        for group_name in cls.list_default_groups_name():
            try:
                Group.objects.get(name=f'{group_name.capitalize()} Group')
            except Group.DoesNotExist:
                Group.objects.create(name=f'{group_name.capitalize()} Group')

    @staticmethod
    def list_default_groups_name() -> list:
        all_default_groups = [StaffMember.default_groups_name, *[subclass.default_groups_name for subclass in StaffMember.__subclasses__()]]
        return list(set(itertools.chain.from_iterable(all_default_groups)))
    

class SaleMember(StaffMember):
    default_groups_name = ['Sale']
    class Meta:
        verbose_name = 'Membres de l\'équipe de vente'


class SupportMember(StaffMember):
    default_groups_name = ['Support']
    class Meta:
        verbose_name = 'Membres de l\'équipe de support'


class ManageMember(StaffMember):
    default_groups_name = ['Manage']
    class Meta:
        verbose_name = 'Membres de l\'équipe de gestion'


StaffMember.link_subclasses()