# from pathlib import Path
# import random
# from faker import Faker
# from django.core.management.base import BaseCommand
# from django.utils.timezone import now
# from django.core.files.base import ContentFile
# from apps.accounts.models import User
# from apps.postsapi.models import Post


# class Command(BaseCommand):
#     help = "Generate random posts using Faker"

#     def handle(self, *args, **kwargs):
#         fake = Faker()

#         # Ensure there are users in the database
#         if not User.objects.exists():
#             self.stdout.write(self.style.ERROR("No users found. Create users first."))
#             return

#         # Number of posts to generate
#         num_posts = random.randint(1, 50)
#         self.stdout.write(f"Generating {num_posts} posts...")

#         # Load the video file once
#         video_path = (
#             Path(__file__).resolve().parent.parent.parent.parent.parent / "default.mp4"
#         )

#         # print(".............>>>>>")
#         # print("video path ,", video_path)
#         # print(Path(__file__).resolve().parent.parent.parent.parent.parent / "default.mp4")
#         # print(".............>>>>>")

#         with open(video_path, "rb") as f:
#             video_bytes = f.read()

#         # Create and save each post
#         for i in range(num_posts):
#             user = User.objects.order_by("?").first()
#             post = Post(
#                 user=user,
#                 text=fake.text(max_nb_chars=200),
#                 created_at=now(),
#                 updated_at=now(),
#             )

#             # Use a unique filename to avoid collision
#             post.video.save(f"default_{i}.mp4", ContentFile(video_bytes), save=True)

#         self.stdout.write(
#             self.style.SUCCESS(f"{num_posts} posts successfully created.")
#         )
