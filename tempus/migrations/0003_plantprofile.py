from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tempus", "0002_contractorprofile"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlantProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("employee_number", models.CharField(blank=True, max_length=40)),
                ("document_number", models.CharField(db_index=True, max_length=40, unique=True)),
                ("full_name", models.CharField(max_length=255)),
                ("area", models.CharField(blank=True, max_length=180)),
                ("studies", models.TextField(blank=True)),
                ("source_row", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="plant_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["full_name", "id"],
            },
        ),
    ]
