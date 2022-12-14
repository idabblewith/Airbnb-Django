# Generated by Django 4.1.2 on 2022-10-16 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("experiences", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="experience",
            old_name="ends_at",
            new_name="end",
        ),
        migrations.RenameField(
            model_name="experience",
            old_name="starts_at",
            new_name="start",
        ),
        migrations.AlterField(
            model_name="perk",
            name="explanation",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="perk",
            name="info",
            field=models.CharField(blank=True, default="", max_length=250),
        ),
    ]
