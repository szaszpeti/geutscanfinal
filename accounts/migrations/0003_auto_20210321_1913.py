# Generated by Django 3.1.7 on 2021-03-21 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210321_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inspection',
            name='technician_one',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.technician'),
        ),
    ]