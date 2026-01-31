
import os
import django
from django.utils import timezone
from datetime import timedelta
import random

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyApp.settings')
django.setup()

from guest.models import CustomUser, Employer, student, Notification, District
from employer.models import Jobposting, Subscription
from student.models import Application, SkillService

def create_dummy_data():
    print("🌱 Starting Database Seeding...")

    # 1. Create Districts
    districts = ['Kochi', 'Trivandrum', 'Calicut', 'Bangalore']
    district_objs = []
    for d in districts:
        obj, created = District.objects.get_or_create(district=d)
        district_objs.append(obj)
    print(f"✅ Verified {len(district_objs)} Districts")

    # 2. Create Employer
    emp_email = "demo_employer@test.com"
    if not CustomUser.objects.filter(email=emp_email).exists():
        emp_user = CustomUser.objects.create_user(
            email=emp_email,
            name="Tech Solutions Inc",
            password="password123",
            role="employer"
        )
        employer = Employer.objects.create(
            user=emp_user,
            company_name="Tech Solutions Inc",
            contact_person="John Doe",
            phone="9876543210",
            email=emp_email,
            district=district_objs[0],
            area="Infopark",
            industry="IT Software",
            address="Building 2, Infopark, Kochi",
            verification_status=True
        )
        print(f"✅ Created Employer: {employer.company_name}")
    else:
        emp_user = CustomUser.objects.get(email=emp_email)
        employer = emp_user.employer_profile
        print(f"ℹ️ Employer {employer.company_name} already exists")

    # 3. Create Jobs
    job_titles = ["Python Jr. Developer", "Frontend React Intern", "Data Entry Specialist"]
    for title in job_titles:
        if not Jobposting.objects.filter(job_title=title, employer=employer).exists():
            Jobposting.objects.create(
                employer=employer,
                job_title=title,
                job_description="This is a great opportunity for students...",
                location="Kochi - Hybrid",
                part_time_category="flexible",
                job_type="offline",
                shift_timing="4 PM - 8 PM",
                working_days="Mon - Fri",
                hourly_pay=500,
                expiry_date=timezone.now() + timedelta(days=30),
                salary_range="10k - 15k"
            )
            print(f"   - Posted Job: {title}")

    # 4. Create Student
    stud_email = "demo_student@test.com"
    if not CustomUser.objects.filter(email=stud_email).exists():
        stud_user = CustomUser.objects.create_user(
            email=stud_email,
            name="Rahul Kumar",
            password="password123",
            role="student"
        )
        student_obj = student.objects.create(
            user=stud_user,
            student_name="Rahul Kumar",
            email=stud_email,
            phone_number="9080706050",
            district=district_objs[1],
            academic_status="Undergraduate",
            skills="Python, Django, HTML"
        )
        print(f"✅ Created Student: {student_obj.student_name}")
        
        # Add Notification for Student
        Notification.objects.create(
            user=stud_user,
            message="Welcome to Learn To Earn! Complete your profile to get started.",
            link="/student/profile/"
        )
    else:
        student_obj = student.objects.get(user__email=stud_email)
        print(f"ℹ️ Student {student_obj.student_name} already exists")

    print("🎉 Database Seeding Completed Successfully!")

if __name__ == '__main__':
    create_dummy_data()
