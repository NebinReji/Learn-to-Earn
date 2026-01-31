
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyProject.settings')
django.setup()

from MyApp.models import District

count = District.objects.count()
print(f"District Count: {count}")
if count > 0:
    print("Districts:", list(District.objects.values_list('district_name', flat=True)))
