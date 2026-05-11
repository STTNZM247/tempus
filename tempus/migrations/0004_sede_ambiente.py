from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tempus", "0003_plantprofile"),
    ]

    operations = [
        migrations.CreateModel(
            name="Sede",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=180, unique=True)),
                ("ubicacion", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["nombre", "id"],
            },
        ),
        migrations.CreateModel(
            name="Ambiente",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=180)),
                ("descripcion", models.CharField(blank=True, max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("sede", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ambientes", to="tempus.sede")),
            ],
            options={
                "ordering": ["sede__nombre", "nombre", "id"],
                "constraints": [models.UniqueConstraint(fields=("sede", "nombre"), name="unique_ambiente_por_sede")],
            },
        ),
    ]
