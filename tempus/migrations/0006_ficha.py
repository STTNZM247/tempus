from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tempus", "0005_profileavatar"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Ficha",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("codigo", models.CharField(db_index=True, max_length=50, unique=True)),
                ("version_programa", models.CharField(blank=True, max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="fichas_creadas", to=settings.AUTH_USER_MODEL),
                ),
                (
                    "matrix",
                    models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="fichas", to="tempus.matrixupload"),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
