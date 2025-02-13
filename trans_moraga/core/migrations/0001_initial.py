# Generated by Django 4.2.7 on 2024-11-26 19:59

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Camiones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patente', models.CharField(max_length=8)),
                ('modelo', models.CharField(max_length=255)),
                ('year', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1970), django.core.validators.MaxValueValidator(2024)])),
                ('tipo_camion', models.CharField(max_length=255)),
                ('marca', models.CharField(max_length=255)),
                ('sigla_base', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Propietario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(blank=True, max_length=255, null=True)),
                ('telefono_contacto', models.CharField(blank=True, max_length=20, null=True)),
                ('firma', models.ImageField(default='Sin Firma', null=True, upload_to='firmas', verbose_name='Firma')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FormularioInspeccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('propietario', models.CharField(max_length=255)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('encuestador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Encuestador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.CharField(blank=True, max_length=255, null=True)),
                ('telefono_contacto', models.CharField(blank=True, max_length=20, null=True)),
                ('firma', models.ImageField(default='Sin Firma', null=True, upload_to='firmas', verbose_name='Firma')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Componente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoria', models.CharField(max_length=255)),
                ('componente', models.CharField(max_length=255)),
                ('inspeccion', models.CharField(choices=[('M', 'Malo'), ('R', 'Regular'), ('B', 'Bueno')], max_length=1)),
                ('observacion', models.TextField(blank=True, null=True)),
                ('formulario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='componentes', to='core.formularioinspeccion')),
            ],
        ),
    ]
