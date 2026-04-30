
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("localevents", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[("Member", "Member"), ("Event Organizer", "Event Organizer")],
                        default="Member",
                        max_length=50,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="event",
            name="event_capacity",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="event",
            name="event_image",
            field=models.ImageField(blank=True, null=True, upload_to="localevents/events/"),
        ),
        migrations.AddField(
            model_name="event",
            name="organizer",
            field=models.ManyToManyField(blank=True, related_name="organized_events", to="localevents.profile"),
        ),
        migrations.AddField(
            model_name="event",
            name="status",
            field=models.CharField(
                choices=[
                    ("Available", "Available"),
                    ("Full", "Full"),
                    ("Done", "Done"),
                    ("Cancelled", "Cancelled"),
                ],
                default="Available",
                max_length=20,
            ),
        ),
        migrations.CreateModel(
            name="EventSignup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("new_registrant", models.CharField(blank=True, max_length=255)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="signups",
                        to="localevents.event",
                    ),
                ),
                (
                    "user_registrant",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="event_signups",
                        to="localevents.profile",
                    ),
                ),
            ],
        ),
    ]
