# Generated by Django 4.2.1 on 2023-06-14 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='managemember',
            options={'verbose_name': "Membres de l'équipe de gestion"},
        ),
        migrations.AlterModelOptions(
            name='salemember',
            options={'verbose_name': "Membres de l'équipe de vente"},
        ),
        migrations.AlterModelOptions(
            name='supportmember',
            options={'verbose_name': "Membres de l'équipe de support"},
        ),
    ]
