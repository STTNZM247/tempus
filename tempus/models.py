from django.conf import settings
from django.db import models


class MatrixUpload(models.Model):
    project_code = models.CharField(max_length=50, unique=True)
    project_description = models.TextField(blank=True)
    program_code = models.CharField(max_length=50, db_index=True)
    program_name = models.CharField(max_length=255)
    level = models.CharField(max_length=50, blank=True)
    version = models.CharField(max_length=20, blank=True)
    competency_count = models.PositiveIntegerField(default=0)
    result_count = models.PositiveIntegerField(default=0)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="matrix_uploads",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.program_name} ({self.project_code})"


class MatrixCompetency(models.Model):
    matrix = models.ForeignKey(MatrixUpload, on_delete=models.CASCADE, related_name="competencies")
    code = models.CharField(max_length=50, blank=True)
    name = models.TextField()
    hours = models.CharField(max_length=20, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]


class MatrixResult(models.Model):
    competency = models.ForeignKey(MatrixCompetency, on_delete=models.CASCADE, related_name="results")
    name = models.TextField()
    hours_max = models.CharField(max_length=20, blank=True)
    hours_min = models.CharField(max_length=20, blank=True)
    trimester = models.CharField(max_length=20, blank=True)
    weekly_hours = models.CharField(max_length=20, blank=True)
    trimester_hours = models.CharField(max_length=20, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]


class ContractorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contractor_profile",
    )
    contract_number = models.CharField(max_length=80, unique=True)
    document_number = models.CharField(max_length=40, unique=True, db_index=True)
    full_name = models.CharField(max_length=255)
    sena_email = models.EmailField(max_length=255, blank=True)
    education_level = models.CharField(max_length=120, blank=True)
    undergraduate = models.TextField(blank=True)
    postgraduate = models.TextField(blank=True)
    coordination = models.CharField(max_length=180, blank=True)
    modality = models.CharField(max_length=120, blank=True)
    specialty = models.TextField(blank=True)
    contract_start_date = models.DateField(null=True, blank=True)
    contract_end_date = models.DateField(null=True, blank=True)
    source_row = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["full_name", "id"]


class PlantProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="plant_profile",
    )
    employee_number = models.CharField(max_length=40, blank=True)
    document_number = models.CharField(max_length=40, unique=True, db_index=True)
    full_name = models.CharField(max_length=255)
    area = models.CharField(max_length=180, blank=True)
    studies = models.TextField(blank=True)
    source_row = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["full_name", "id"]


class ProfileAvatar(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile_avatar",
    )
    image = models.ImageField(upload_to="profile_avatars/")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at", "id"]

    def __str__(self):
        return f"Avatar de {self.user.get_username()}"


class Ficha(models.Model):
    ESTADO_ABIERTA = "abierta"
    ESTADO_CERRADA = "cerrada"
    ESTADO_CHOICES = [
        (ESTADO_ABIERTA, "Abierta"),
        (ESTADO_CERRADA, "Cerrada"),
    ]

    JORNADA_DIURNA = "diurna"
    JORNADA_MIXTA_18_22 = "mixta_18_22"
    JORNADA_MIXTA_16_22 = "mixta_16_22"
    JORNADA_FINES_SEMANA = "fines_semana"
    JORNADA_CHOICES = [
        (JORNADA_DIURNA, "Diurna"),
        (JORNADA_MIXTA_18_22, "Mixta de 18:00 a 22:00"),
        (JORNADA_MIXTA_16_22, "Mixta de 16:00 a 22:00"),
        (JORNADA_FINES_SEMANA, "Fines de semana"),
    ]

    codigo = models.CharField(max_length=50, unique=True, db_index=True)
    matrix = models.ForeignKey(MatrixUpload, on_delete=models.PROTECT, related_name="fichas")
    version_programa = models.CharField(max_length=20, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default=ESTADO_ABIERTA)
    cdf_trimestres = models.PositiveSmallIntegerField(null=True, blank=True)
    jornada = models.CharField(max_length=20, choices=JORNADA_CHOICES, default=JORNADA_DIURNA)
    fecha_inicio_lectiva = models.DateField(null=True, blank=True)
    fecha_fin_lectiva = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="fichas_creadas",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Ficha {self.codigo}"


class Sede(models.Model):
    nombre = models.CharField(max_length=180, unique=True)
    ubicacion = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre", "id"]

    def __str__(self):
        return self.nombre


class Ambiente(models.Model):
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name="ambientes")
    nombre = models.CharField(max_length=180)
    descripcion = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["sede__nombre", "nombre", "id"]
        constraints = [
            models.UniqueConstraint(fields=["sede", "nombre"], name="unique_ambiente_por_sede"),
        ]

    def __str__(self):
        return f"{self.sede.nombre} - {self.nombre}"
