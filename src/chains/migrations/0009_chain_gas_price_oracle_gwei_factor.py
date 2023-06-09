# Generated by Django 3.2.5 on 2021-07-09 13:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chains", "0008_chain_ens_registry_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="chain",
            name="gas_price_oracle_gwei_factor",
            field=models.DecimalField(
                decimal_places=9,
                default=1,
                help_text="Factor required to reach the Gwei unit",
                max_digits=19,
                verbose_name="Gwei multiplier factor",
            ),
        ),
    ]
