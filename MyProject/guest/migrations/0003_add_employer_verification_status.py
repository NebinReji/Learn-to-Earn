from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("guest", "0002_add_jobposting"),
    ]

    operations = [
        migrations.AddField(
            model_name="employer",
            name="verification_status",
            field=models.BooleanField(default=False),
        ),
    ]
