# Generated by Django 4.2.1 on 2023-05-18 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("test2", "0014_alter_customer_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Out of delivery", "Out of delivery"),
                    ("Delivered", "Delivered"),
                ],
                max_length=200,
                null=True,
            ),
        ),
    ]
