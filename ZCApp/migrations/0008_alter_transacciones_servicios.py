# Generated by Django 4.2.5 on 2023-12-25 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ZCApp', '0007_transacciones'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transacciones',
            name='servicios',
            field=models.ManyToManyField(related_name='transacciones', to='ZCApp.solicitud_servicios'),
        ),
    ]