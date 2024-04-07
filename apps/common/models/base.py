from django.db import models
import uuid


class BaseModel(models.Model):
    """Base model with slug field ref."""
    id = models.UUIDField(
        'ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    ref = models.SlugField(
        'REF.',
        unique=True,
        max_length=100,
        blank=False,
        null=False,
        help_text='This attribute should be unique.'
    )
    available = models.BooleanField(
        'Disponible',
        default=True
    )
    created = models.DateTimeField(
        'Fecha de creación',
        auto_now=False,
        auto_now_add=True
    )
    modified = models.DateTimeField(
        'Fecha de modificación',
        auto_now=True,
        auto_now_add=False
    )

    class Meta:
        abstract = True
        verbose_name = 'Base Model Ref'


class BaseModelNotRef(models.Model):
    """Base model without slug field ref."""
    id = models.UUIDField(
        'ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    available = models.BooleanField(
        'Disponible',
        default=True
    )
    created = models.DateTimeField(
        'Fecha de creación',
        auto_now=False,
        auto_now_add=True
    )
    modified = models.DateTimeField(
        'Fecha de modificación',
        auto_now=True,
        auto_now_add=False
    )

    class Meta:
        abstract = True
        verbose_name = 'Base Model Not Ref'


