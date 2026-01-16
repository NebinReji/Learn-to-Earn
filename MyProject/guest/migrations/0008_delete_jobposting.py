from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0007_customuser_role'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Jobposting',
        ),
    ]
