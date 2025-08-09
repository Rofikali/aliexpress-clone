# from django.core.management.base import BaseCommand
# from apps.products.models import Products
# from faker import Faker
# import random
# import os
# from django.core.files.base import ContentFile
# from PIL import Image
# from io import BytesIO

# fake = Faker()


# class Command(BaseCommand):
#     help = "Generate fake products for testing"

#     def add_arguments(self, parser):
#         parser.add_argument(
#             "total", type=int, help="The number of fake products to create"
#         )

#     def handle(self, *args, **kwargs):
#         total = kwargs["total"]

#         for _ in range(total):
#             # Generate a random product title & description
#             title = fake.sentence(nb_words=4)
#             description = fake.paragraph(nb_sentences=5)
#             price = random.randint(10, 1000)

#             # Create a placeholder image
#             image_content = self.generate_image()

#             product = Products(title=title, description=description, price=price)
#             # img =
#             product.image.save(f"{fake.word()}.png", image_content, save=True)

#         self.stdout.write(
#             self.style.SUCCESS(f"✅ Successfully created {total} fake products.")
#         )

#     def generate_image(self):
#         """Generate a simple placeholder image in memory."""
#         img = Image.new(
#             "RGB",
#             (300, 300),
#             color=(
#                 random.randint(0, 255),
#                 random.randint(0, 255),
#                 random.randint(0, 255),
#             ),
#         )
#         buffer = BytesIO()
#         img.save(buffer, format="PNG")
#         return ContentFile(buffer.getvalue())

from django.core.management.base import BaseCommand
from django.core.files import File
from apps.products.models import Products
from faker import Faker
import random
from pathlib import Path

fake = Faker()


class Command(BaseCommand):
    help = "Generate fake products using default image"

    def add_arguments(self, parser):
        parser.add_argument(
            "total", type=int, help="The number of fake products to create"
        )

    def handle(self, *args, **kwargs):
        total = kwargs["total"]
        created = 0

        # Path to default.jpg (place this file in project root or wherever you prefer)
        image_path = (
            Path(__file__).resolve().parent.parent.parent.parent.parent / "default.jpg"
        )

        print(f"Using image path: {image_path}")

        if not image_path.exists():
            self.stdout.write(
                self.style.ERROR(f"Image file not found: {image_path}. Aborting.")
            )
            return

        for i in range(total):
            title = f"Product {i + 1}"
            description = fake.paragraph(nb_sentences=5)
            price = random.randint(50, 5000)

            with open(image_path, "rb") as img_file:
                django_file = File(img_file, name=image_path.name)

                Products.objects.create(
                    title=title, description=description, price=price, image=django_file
                )
                created += 1
                self.stdout.write(self.style.SUCCESS(f"✅ Created product: {title}"))

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Done. {created} products created."))
