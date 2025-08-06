# import random
# from django.core.management.base import BaseCommand
# from faker import Faker
# from django.contrib.auth import get_user_model
# # from your_app.models import Like, Post  # Replace 'your_app' with your actual app name
# from apps.postsapi.models import Post
# from apps.like.models import Like

# User = get_user_model()
# fake = Faker()

# class Command(BaseCommand):
#     help = "Create 20 random likes using Faker"

#     def handle(self, *args, **kwargs):
#         users = list(User.objects.all())
#         posts = list(Post.objects.all())

#         if not users or not posts:
#             self.stdout.write(self.style.ERROR("Ensure there are users and posts in the database first."))
#             return

#         created = 0
#         attempts = 0

#         while created < 20 and attempts < 100:
#             user = random.choice(users)
#             post = random.choice(posts)

#             # Avoid duplicate likes
#             if Like.objects.filter(user=user, post=post).exists():
#                 attempts += 1
#                 continue

#             Like.objects.create(user=user, post=post)
#             created += 1

#         self.stdout.write(self.style.SUCCESS(f"Successfully created {created} fake likes."))
