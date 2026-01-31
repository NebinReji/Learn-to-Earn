
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyProject.settings')
django.setup()

from MyApp.models import District

districts = [
    "Thiruvananthapuram", "Kollam", "Pathanamthitta", "Alappuzha", 
    "Kottayam", "Idukki", "Ernakulam", "Thrissur", "Palakkad", 
    "Malappuram", "Kozhikode", "Wayanad", "Kannur", "Kasaragod"
]

for d_name in districts:
    obj, created = District.objects.get_or_create(district_name=d_name)
    if created:
        print(f"Added {d_name}")
    else:
        print(f"Skipped {d_name} (already exists)")
