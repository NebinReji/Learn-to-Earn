from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('guest', '0006_remove_employer_jobs_posted_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Jobposting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=200)),
                ('job_description', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('work_mode', models.CharField(max_length=50)),
                ('posted_date', models.DateField(auto_now_add=True)),
                ('expiry_date', models.DateField()),
                ('salary_range', models.CharField(max_length=100)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_postings', to='guest.employer')),
            ],
            options={
                'verbose_name': 'Job Posting',
                'verbose_name_plural': 'Job Postings',
                'ordering': ['-posted_date'],
            },
        ),
    ]
