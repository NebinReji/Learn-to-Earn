import os
import django
import random
from datetime import timedelta
from django.utils import timezone
from django.core.files.base import ContentFile

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyProject.settings')
django.setup()

from guest.models import CustomUser, student, Employer
from MyApp.models import District, Category
from employer.models import Jobposting
from student.models import SkillService

def run():
    print("--- Starting Data Population ---")

    # 1. Populate Districts
    districts = [
        "Thiruvananthapuram", "Kollam", "Pathanamthitta", "Alappuzha", 
        "Kottayam", "Idukki", "Ernakulam", "Thrissur", "Palakkad", 
        "Malappuram", "Kozhikode", "Wayanad", "Kannur", "Kasaragod"
    ]
    district_objs = []
    for d_name in districts:
        obj, created = District.objects.get_or_create(district_name=d_name)
        district_objs.append(obj)
    print(f"Verified {len(district_objs)} districts.")

    # 2. Populate Categories
    categories = [
        "IT & Software", "Education & Tutoring", "Retail & Sales", 
        "Events & Hospitality", "Marketing & Content", "Design & Creative", "Other"
    ]
    category_objs = []
    for c_name in categories:
        obj, created = Category.objects.get_or_create(category_name=c_name)
        category_objs.append(obj)
    print(f"Verified {len(category_objs)} categories.")

    # 3. Create Students
    students_data = [
        {
            "name": "Arjun Kumar",
            "email": "arjun@example.com",
            "phone": "9876543210",
            "district": "Ernakulam",
            "skills": "Python, Django, Web Development",
            "services": [
                {"title": "Python Tutoring", "cat": "tuition", "price": 500, "desc": "I can teach you Python basics to advanced concepts."},
                {"title": "Django Web App Build", "cat": "technical", "price": 5000, "desc": "Build responsive web application."}
            ]
        },
        {
            "name": "Sneha Menon",
            "email": "sneha@example.com",
            "phone": "8765432109",
            "district": "Thiruvananthapuram",
            "skills": "Graphic Design, content writing, Illustration",
            "services": [
                {"title": "Logo Design Service", "cat": "creative", "price": 1500, "desc": "Professional logo design with 3 revisions."},
                {"title": "Blog Content Writing", "cat": "writing", "price": 300, "desc": "High quality SEO optimized blog posts (500 words)."}
            ]
        },
        {
            "name": "Rahul Nair",
            "email": "rahul@example.com",
            "phone": "7654321098",
            "district": "Kozhikode",
            "skills": "Event Management, Catering Support",
            "services": [
                {"title": "Event Coordination", "cat": "other", "price": 1000, "desc": "Assistance in managing small to medium events."}
            ]
        }
    ]

    print("\nCreating Students...")
    for s_data in students_data:
        user, created = CustomUser.objects.get_or_create(email=s_data['email'])
        if created:
            user.name = s_data['name']
            user.set_password("password123")
            user.role = 'student'
            user.save()
            print(f"Created Student User: {s_data['email']}")
        
        # Create/Update Student Profile
        dist_obj = District.objects.get(district_name=s_data['district'])
        stud_profile, created = student.objects.get_or_create(user=user)
        stud_profile.student_name = s_data['name']
        stud_profile.email = s_data['email']
        stud_profile.phone_number = s_data['phone']
        stud_profile.district = dist_obj
        stud_profile.skills = s_data['skills']
        stud_profile.verification_status = True # Auto-verify for demo
        # Mock ID card file if checking is strict, but usually file fields can be empty/strings if not accessed strictly
        stud_profile.save()

        # Create Services
        if created or not stud_profile.services.exists():
            for svc in s_data['services']:
                SkillService.objects.create(
                    student=stud_profile,
                    title=svc['title'],
                    description=svc['desc'],
                    category=svc['cat'],
                    price=svc['price'],
                    verification_status='verified'
                )
            print(f" - Added services for {s_data['name']}")

    # 4. Create Employers
    employers_data = [
        {
            "name": "TechSolutions Inc", # Company Name
            "contact": "John Doe",
            "email": "hr@techsolutions.com",
            "phone": "0484222333",
            "district": "Ernakulam",
            "jobs": [
                {
                    "title": "Junior Python Intern", 
                    "desc": "Looking for a smart student to help with backend scripts.",
                    "type": "remote", "cat": "technical", "pay": 8000
                }
            ]
        },
        {
            "name": "Kochi Events",
            "contact": "Sarah Thomas",
            "email": "sarah@kochevents.com",
            "phone": "0484222444",
            "district": "Kochi", # Will map to Ernakulam if not strictly matched, assuming Ernakulam for now or specific district
            "jobs": [
                {
                    "title": "Weekend Event Usher", 
                    "desc": "Need energetic students for weekend wedding events.",
                    "type": "offline", "cat": "event", "pay": 1000
                },
                {
                    "title": "Social Media Manager", 
                    "desc": "Manage our Instagram page.",
                    "type": "remote", "cat": "creative", "pay": 5000
                }
            ]
        }
    ]

    print("\nCreating Employers...")
    for e_data in employers_data:
        user, created = CustomUser.objects.get_or_create(email=e_data['email'])
        if created:
            user.name = e_data['contact']
            user.set_password("password123")
            user.role = 'employer'
            user.save()
            print(f"Created Employer User: {e_data['email']}")

        # Handle district mapping (simple fallback)
        try:
            dist_obj = District.objects.get(district_name=e_data['district'])
        except District.DoesNotExist:
             dist_obj = District.objects.first()

        emp_profile, created = Employer.objects.get_or_create(user=user)
        emp_profile.company_name = e_data['name']
        emp_profile.contact_person = e_data['contact']
        emp_profile.email = e_data['email']
        emp_profile.phone = e_data['phone']
        emp_profile.district = dist_obj
        emp_profile.verification_status = True
        emp_profile.save()

        # Create Jobs
        if created or not emp_profile.job_postings.exists():
            for job in e_data['jobs']:
                Jobposting.objects.create(
                    employer=emp_profile,
                    job_title=job['title'],
                    job_description=job['desc'],
                    location=dist_obj.district_name,
                    job_type=job['type'],
                    hourly_pay=job.get('pay', 0) if job.get('pay', 0) < 1000 else 0, # Hacky logic for hourly vs salary, just setting fields
                    salary_range=f"INR {job.get('pay')}",
                    expiry_date=timezone.now() + timedelta(days=30)
                )
            print(f" - Added jobs for {e_data['name']}")

    print("\n--- Data Population Complete ---")
    print("Credentials:")
    print("All Passwords: password123\n")
    print("STUDENTS:")
    for s in students_data:
        print(f" - {s['email']}")
    print("\nEMPLOYERS:")
    for e in employers_data:
        print(f" - {e['email']}")

if __name__ == '__main__':
    run()
