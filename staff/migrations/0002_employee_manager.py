# Generated by Django 4.1.4 on 2022-12-16 11:53

from django.db import migrations, models
import django.db.models.deletion
import random


def add_manager(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Employee = apps.get_model("staff", "Employee")
    manager = Employee.objects.order_by("?").first()
    population = Employee.objects.exclude(id=manager.id).values_list(
        "id", flat=True
    )
    subordinates = random.sample(sorted(population), 5)
    for subordinate in Employee.objects.filter(id__in=subordinates):
        subordinate.manager = manager
        subordinate.save()


class Migration(migrations.Migration):

    dependencies = [
        ("staff", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="manager",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="staff.employee",
            ),
        ),
        migrations.RunPython(add_manager),
    ]
