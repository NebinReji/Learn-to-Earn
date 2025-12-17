# Generated migration to add Jobposting model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobposting',
            fields=[
                ('job_id', models.AutoField(primary_key=True, serialize=False)),
                ('job_title', models.CharField(max_length=200)),
                ('job_description', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('work_mode', models.CharField(max_length=50)),
                ('posted_date', models.DateField(auto_now_add=True)),
                ('expiry_date', models.DateField()),
                ('salary_range', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('employer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_postings', to='guest.employer')),
            ],
        ),
    ]
