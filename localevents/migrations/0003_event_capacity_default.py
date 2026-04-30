from django.db import migrations, models


def set_default_capacity(apps, schema_editor):
    Event = apps.get_model("localevents", "Event")
    Event.objects.filter(event_capacity=0).update(event_capacity=1)


class Migration(migrations.Migration):

    dependencies = [
        ("localevents", "0002_localevents_expanded"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="event_capacity",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.RunPython(set_default_capacity, migrations.RunPython.noop),
    ]
