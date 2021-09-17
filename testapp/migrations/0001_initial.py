from django.db import migrations, models

def initialize_choices(apps, schema_editor):
    ChoicesModel = apps.get_model('testapp', 'ChoicesModel')
    for counter in range(999):
        label = f"Option {counter + 100}"
        ChoicesModel.objects.create(tenant=1, label=label)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PayloadModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='ChoicesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant', models.PositiveSmallIntegerField()),
                ('label', models.CharField(max_length=50, verbose_name='Choice')),
            ],
            options={
                'unique_together': {('tenant', 'label')},
            },
        ),
        migrations.RunPython(initialize_choices),
    ]
