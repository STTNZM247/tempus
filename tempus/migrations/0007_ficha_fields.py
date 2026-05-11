from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tempus", "0006_ficha"),
    ]

    operations = [
        migrations.AddField(
            model_name="ficha",
            name="cdf_trimestres",
            field=models.PositiveSmallIntegerField(default=5),
        ),
        migrations.AddField(
            model_name="ficha",
            name="estado",
            field=models.CharField(choices=[("abierta", "Abierta"), ("cerrada", "Cerrada")], default="abierta", max_length=10),
        ),
        migrations.AddField(
            model_name="ficha",
            name="fecha_fin_lectiva",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="ficha",
            name="fecha_inicio_lectiva",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="ficha",
            name="jornada",
            field=models.CharField(
                choices=[
                    ("diurna", "Diurna"),
                    ("mixta_18_22", "Mixta de 18:00 a 22:00"),
                    ("mixta_16_22", "Mixta de 16:00 a 22:00"),
                    ("fines_semana", "Fines de semana"),
                ],
                default="diurna",
                max_length=20,
            ),
        ),
    ]
