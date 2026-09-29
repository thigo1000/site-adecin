from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pgm', '0003_alter_pgm_horario'),
    ]

    operations = [
        migrations.AddField(
            model_name='pgm',
            name='categoria',
            field=models.CharField(
                choices=[
                    ('mulheres', 'Mulheres'),
                    ('homens', 'Homens'),
                    ('jovens', 'Jovens'),
                    ('adolescentes', 'Adolescentes'),
                    ('juniores', 'Juniores'),
                ],
                default='',
                max_length=20,
            ),
            preserve_default=False,
        ),
    ]