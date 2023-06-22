from django.db import models

# Create your models here.

from phonenumber_field.modelfields import PhoneNumberField
from authentication.models import SaleMember, SupportMember

class Company(models.Model):
    first_name = models.CharField(verbose_name='Prenom', max_length=25)
    last_name = models.CharField(verbose_name='Nom', max_length=25)
    email = models.EmailField(verbose_name='Email', unique=True)
    phone = PhoneNumberField(verbose_name='Telephone fix')
    mobile = PhoneNumberField(verbose_name='Telephone portable', blank=True)
    company_name = models.CharField(verbose_name='Non d\'entreprise', max_length=250)
    date_created = models.DateTimeField(verbose_name='Date de création', auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name='Dernière mise à jour', auto_now=True)

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

class Client(Company):
    sale_contact = models.ForeignKey(
        verbose_name='Conseiller(ère)',
        to=SaleMember,
        related_name='Clients',
        on_delete=models.CASCADE
    )
    
    def __str__(self) -> str:
        return f'{self.last_name} {self.first_name}:{self.company_name}'
    
    class Meta:
        verbose_name = 'Client'

class Prospect(Company):
    def to_client(self, sale_contact):
        data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'mobile': self.mobile,
            'company_name': self.company_name,
            'date_created': self.date_created,
            'date_updated': self.date_updated,
            'sale_contact': sale_contact
        }
        self.delete()
        return Client.objects.create(**data)

    class Meta:
        verbose_name = 'Prospect'


class Contract(models.Model):
    client = models.ForeignKey(
        to=Client,
        related_name='contracts',
        on_delete=models.CASCADE,
        verbose_name='Client',
        blank=False
    )
    status = models.BooleanField(
        verbose_name='statut',
        default=False
    )
    amount = models.FloatField(
        verbose_name='Montant'
    )
    payment_due = models.DateTimeField(
        verbose_name='Date de paiement'
    )
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    date_updated = models.DateTimeField(
        auto_now=True
    )
    @property
    def sale_contact(self):
        return self.client.sale_contact
    
    @property
    def client_company_name(self):
        return self.client.company_name
    
    client_company_name.fget.short_description = 'Nom d\'entreprise du contrat'
    
    class Meta:
        verbose_name = 'Contrat'


class Event(models.Model):
    support_contact = models.ForeignKey(
        to=SupportMember,
        related_name='events',
        on_delete=models.CASCADE,
        verbose_name='Support',
        blank=True
    )
    event_status = models.OneToOneField(
        to=Contract,
        related_name='event',
        on_delete=models.CASCADE,
        verbose_name='Contrat',
        blank=False
    )
    date_created = models.DateTimeField(
        verbose_name='Date de creation',
        auto_now_add=True
    )
    date_updated = models.DateTimeField(
        verbose_name='Date de mise à jour',
        auto_now=True
    )
    event_date = models.DateTimeField(
        verbose_name='Date de l\'évenement'
    )
    notes = models.TextField(
        verbose_name='Notes'
    )
    attendees = models.IntegerField(
        verbose_name='Participants(es)'
    )

    @property
    def client(self):
        return self.event_status.client
    
    @property
    def sale_contact(self):
        return self.event_status.sale_contact

    client.fget.short_description = 'Nom d\'entreprise de l\'évenement'
    sale_contact.fget.short_description = 'Conseiller(ère) du contrat'

    class Meta:
        verbose_name = 'Évenement'

Company.link_subclasses()
