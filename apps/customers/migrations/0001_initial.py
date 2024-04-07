# Generated by Django 4.2 on 2024-04-07 19:03

from django.db import migrations, models
import django.db.models.deletion
import django_tenants.postgresql_backend.base
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('schema_name', models.CharField(db_index=True, max_length=63, unique=True, validators=[django_tenants.postgresql_backend.base._check_schema_name])),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('paid_until', models.DateField()),
                ('on_trial', models.BooleanField()),
                ('created_on', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Client',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('available', models.BooleanField(default=True, verbose_name='Disponible')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('ref', models.SlugField(max_length=100, null=True, verbose_name='Ref')),
                ('description', models.CharField(max_length=255, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Payment Method',
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=253, unique=True)),
                ('is_primary', models.BooleanField(db_index=True, default=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='customers.client')),
            ],
            options={
                'verbose_name': 'Domain',
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('available', models.BooleanField(default=True, verbose_name='Disponible')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Fecha de modificación')),
                ('nit', models.CharField(blank=True, max_length=10, null=True, verbose_name='NIT')),
                ('responsible_billing', models.CharField(blank=True, max_length=255, null=True, verbose_name='Responsable Facturación')),
                ('city', models.CharField(default='Cali', max_length=255, verbose_name='Ciudad')),
                ('department', models.CharField(default='Valle del Cauca', max_length=255, verbose_name='Departamento')),
                ('billing_address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Dirección Facturación')),
                ('electronic_billing', models.BooleanField(default=True, verbose_name='¿Factura Electrónica?')),
                ('phone', models.CharField(blank=True, max_length=10, null=True, verbose_name='Teléfono')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Correo')),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.domain', verbose_name='Host Tenant')),
                ('payment_method', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.paymentmethod', verbose_name='Método de pago')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.client', verbose_name='Tenant')),
            ],
            options={
                'verbose_name': 'Cuenta',
            },
        ),
    ]