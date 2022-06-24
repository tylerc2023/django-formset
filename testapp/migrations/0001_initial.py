from django.db import migrations, models
import django.db.models.deletion


def initialize_opinions(apps, schema_editor):
    OpinionModel = apps.get_model('testapp', 'OpinionModel')
    for counter in range(1, 1000):
        label = f"Opinion {counter:04}"
        OpinionModel.objects.create(tenant=1, label=label)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OpinionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tenant', models.PositiveSmallIntegerField()),
                ('label', models.CharField(max_length=50, verbose_name='Opinion')),
            ],
            options={
                'unique_together': {('tenant', 'label')},
            },
        ),
        migrations.CreateModel(
            name='PayloadModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='PollModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='WeightedOpinion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.BigIntegerField(default=0, verbose_name='Weighted Opinion')),
                ('opinion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.opinionmodel')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testapp.pollmodel')),
            ],
        ),
        migrations.AddField(
            model_name='pollmodel',
            name='weighted_opinions',
            field=models.ManyToManyField(through='testapp.WeightedOpinion', to='testapp.OpinionModel', verbose_name='Weighted Opinions'),
        ),
        migrations.CreateModel(
            name='PersonModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50, verbose_name='Full Name')),
                ('avatar', models.FileField(blank=True, upload_to='images')),
                ('gender', models.CharField(choices=[('female', 'Female'), ('male', 'Male')], default=None, max_length=10, verbose_name='Gender')),
                ('birth_date', models.DateField(verbose_name='Birth Date')),
                ('continent', models.IntegerField(choices=[(1, 'America'), (2, 'Europe'), (3, 'Asia'), (4, 'Africa'), (5, 'Australia'), (6, 'Oceania'), (7, 'Antartica')], verbose_name='Continent')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(db_index=True, editable=False, max_length=40)),
                ('opinion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persons', to='testapp.opinionmodel', verbose_name='Opinion')),
                ('opinions', models.ManyToManyField(related_name='person_groups', to='testapp.OpinionModel', verbose_name='Opinions')),
            ],
        ),
        migrations.RunPython(initialize_opinions, reverse_code=migrations.RunPython.noop),
    ]
