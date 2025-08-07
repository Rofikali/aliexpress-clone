# from pathlib import Path

# from apps.accounts.models import User
# from django.contrib.auth import get_user_model
# from django.core.files import File
# from django.core.management.base import BaseCommand
# from faker import Faker

# User = get_user_model()  # Use the custom user model defined in settings
# fake = Faker()


# class Command(BaseCommand):
#     help = "Create 20 fake users for testing"

#     def handle(self, *args, **kwargs):
#         count = 20  # 🔴 change this number if needed
#         created = 0

#         # Path to the default image
#         image_path = (
#             Path(__file__).resolve().parent.parent.parent.parent / "default.jpg"
#         )

#         if not image_path.exists():
#             self.stdout.write(
#                 self.style.ERROR(f"Image file not found: {image_path}. Aborting.")
#             )
#             return

#         for _ in range(count):
#             email = fake.unique.email()
#             # username = fake.user_name()
#             # username =
#             # i wnat micky_1, _2 like this
#             username = (
#                 f"admin{_ + 1}"  # Generates usernames like micky_1, micky_2, etc.
#             )
#             name = fake.name()
#             password = "password123"  # 🔴 change this password if needed

#             # Open image file and wrap in Django File
#             with open(image_path, "rb") as img_file:
#                 django_file = File(img_file, name=image_path.name)

#                 if not User.objects.filter(email=email).exists():
#                     User.objects.create_user(
#                         email=email,
#                         username=username,
#                         name=name,
#                         password=password,
#                         bio=fake.text(max_nb_chars=20),
#                         image=django_file,
#                     )
#                     created += 1
#                     self.stdout.write(self.style.SUCCESS(f"✅ Created user: {email}"))

#         self.stdout.write(self.style.SUCCESS(f"\n🎉 Done. {created} users created."))
