from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0006_remove_employer_jobs_posted_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(
                choices=[('admin', 'Admin'), ('employer', 'Employer'), ('student', 'Student')],
                default='student',
                max_length=20
            ),
        ),
    ]
