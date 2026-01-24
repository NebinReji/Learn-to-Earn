
import os
import django
import sys

# Setup Django Environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyProject.settings')
django.setup()

from MyApp.models import Category, Subcategory

def seed_categories():
    print("Seeding Categories and Subcategories...")

    # Data Structure: {Category: [Subcategories]}
    data = {
        "IT & Software": [
            "Web Development", "App Development", "Data Science", 
            "Cybersecurity", "DevOps", "Software Testing"
        ],
        "Design & Creative": [
            "Graphic Design", "UI/UX Design", "Video Editing", 
            "Animation", "Photography", "logo Design"
        ],
        "Sales & Marketing": [
            "Digital Marketing", "SEO Specialist", "Content Marketing", 
            "Social Media Management", "Sales Representative"
        ],
        "Writing & Translation": [
            "Content Writing", "Copywriting", "Translation", 
            "Technical Writing", "Proofreading"
        ],
        "Education & Training": [
            "Online Tutoring", "Language Training", "Exam Coaching", 
            "Corporate Training"
        ],
        "Finance & Accounting": [
            "Accounting", "Financial Analysis", "Bookkeeping", 
            "Tax Consulting"
        ],
        "Admin & Customer Support": [
            "Data Entry", "Virtual Assistant", "Customer Support", 
            "Project Management"
        ],
        "Healthcare & Medical": [
            "Nursing", "Medical Transcription", "Pharmacy", 
            "Lab Technician"
        ],
        "Engineering & Architecture": [
            "Civil Engineering", "Mechanical Engineering", "Interior Design", 
            "CAD Drafting"
        ],
        "Legal Services": [
            "Legal Consulting", "Document Review", "Paralegal Services", 
            "Contract Drafting", "Intellectual Property"
        ],
        "Hospitality & Tourism": [
            "Hotel Management", "Event Planning", "Tour Guide", 
            "Travel Consultant", "Catering Service"
        ],
        "Manufacturing & Logistics": [
            "Supply Chain Management", "Inventory Control", "Quality Assurance", 
            "Logistics Coordinator"
        ]
    }

    for cat_name, subcats in data.items():
        # Create or Get Category
        category, created = Category.objects.get_or_create(category_name=cat_name)
        if created:
            print(f"Created Category: {cat_name}")
        else:
            print(f"Category Exists: {cat_name}")

        # Create Subcategories
        for sub_name in subcats:
            sub, sub_created = Subcategory.objects.get_or_create(
                subcategory_name=sub_name,
                category=category
            )
            if sub_created:
                print(f"   -> Added Subcategory: {sub_name}")

    print("Category Seeding Completed!")

if __name__ == '__main__':
    seed_categories()
