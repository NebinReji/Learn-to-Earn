import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyProject.settings')
django.setup()

from django.contrib.auth import authenticate
from guest.models import CustomUser

# Get all users
users = CustomUser.objects.all()
print(f"\n=== Total users in database: {users.count()} ===\n")

for user in users:
    print(f"Email: {user.email}")
    print(f"  - Is Staff: {user.is_staff}")
    print(f"  - Is Superuser: {user.is_superuser}")
    print(f"  - Has usable password: {user.has_usable_password()}")
    print()

# Test authentication with different passwords
test_email = "admin@gmail.com"
test_passwords = ["admin", "admin123", "password", "test123", "Admin@123"]

print(f"\n=== Testing authentication for {test_email} ===\n")
user = CustomUser.objects.get(email=test_email)

for pwd in test_passwords:
    # Test password check
    check_result = user.check_password(pwd)
    print(f"check_password('{pwd}'): {check_result}")
    
    # Test authenticate
    auth_result = authenticate(username=test_email, password=pwd)
    print(f"authenticate(username='{test_email}', password='{pwd}'): {auth_result}")
    print()

print("\n=== Test other user ===")
test_email2 = "nebinreji2004@gmail.com"
print(f"Testing: {test_email2}")
for pwd in ["password", "test123", "nebin", "Nebin@123"]:
    auth_result = authenticate(username=test_email2, password=pwd)
    print(f"  password '{pwd}': {auth_result}")
