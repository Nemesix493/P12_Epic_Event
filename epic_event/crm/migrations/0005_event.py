# Generated by Django 4.2.1 on 2023-06-22 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_managemember_options_alter_salemember_options_and_more'),
        ('crm', '0004_alter_company_company_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date de creation')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date de mise à jour')),
                ('event_date', models.DateTimeField(verbose_name="Date de l'évenement")),
                ('notes', models.TextField(verbose_name='Notes')),
                ('attendees', models.IntegerField(verbose_name='Participants(es)')),
                ('event_status', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='event', to='crm.contract', verbose_name='Contrat')),
                ('support_contact', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='authentication.supportmember', verbose_name='Support')),
            ],
            options={
                'verbose_name': 'Évenement',
            },
        ),
    ]
