# Generated by Django 3.2.5 on 2021-07-13 08:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("chains", "0010_chain_min_master_copy_version"),
    ]

    operations = [
        migrations.RenameField(
            model_name="chain",
            old_name="min_master_copy_version",
            new_name="recommended_master_copy_version",
        ),
    ]
