import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth import get_user_model
# from your_app.models import Comment, Post  # Replace 'your_app' with your actual app name
from apps.postsapi.models import Post
from apps.comments.models import Comment

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = "Create 20 fake comments using Faker"

    def handle(self, *args, **kwargs):
        users = list(User.objects.all())
        posts = list(Post.objects.all())

        if not users or not posts:
            self.stdout.write(self.style.ERROR("Please ensure you have users and posts in the database."))
            return

        created = 0
        attempts = 0

        while created < 20 and attempts < 100:
            user = random.choice(users)
            post = random.choice(posts)
            text = fake.paragraph(nb_sentences=2).strip()

            # Skip empty or whitespace-only comments
            if not text:
                attempts += 1
                continue

            try:
                comment = Comment(user=user, post=post, text=text)
                comment.full_clean()  # To trigger the `clean()` method
                comment.save()
                created += 1
            except Exception as e:
                attempts += 1
                continue

        self.stdout.write(self.style.SUCCESS(f"Successfully created {created} fake comments."))
