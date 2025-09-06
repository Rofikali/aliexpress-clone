# # # apps/accounts/management/commands/generate_products_json.py
# import json
# import uuid
# import random
# from pathlib import Path
# from django.core.management.base import BaseCommand
# from faker import Faker

# fake = Faker()


# class Command(BaseCommand):
#     help = "Generate fake products JSON file"

#     def add_arguments(self, parser):
#         parser.add_argument("output_path", type=str, help="Where to save the JSON file")
#         parser.add_argument(
#             "--count", type=int, default=100, help="How many products to generate"
#         )

#     def handle(self, *args, **options):
#         output_path = Path(options["output_path"])
#         count = options["count"]

#         products = []
#         for i in range(count):
#             products.append(
#                 {
#                     "id": str(uuid.uuid4()),
#                     "title": fake.unique.sentence(nb_words=3).replace(".", ""),
#                     "slug": fake.unique.slug(),
#                     "description": fake.text(max_nb_chars=200),
#                     "sku": fake.unique.ean(length=13),
#                     "price": round(random.uniform(10, 500), 2),
#                     "discount_price": (
#                         round(random.uniform(5, 400), 2)
#                         if random.choice([True, False])
#                         else None
#                     ),
#                     "currency": "USD",
#                     "stock": random.randint(1, 500),
#                     "is_active": True,
#                     "rating": round(random.uniform(1, 5), 1),
#                     "review_count": random.randint(0, 1000),
#                     "seller_id": 1,  # valid User.id
#                     "category_id": None,  # let import assign Default Category
#                     "brand_id": None,  # let import assign Default Brand
#                 }
#             )

#         with open(output_path, "w", encoding="utf-8") as f:
#             json.dump(products, f, indent=4)

#         self.stdout.write(
#             self.style.SUCCESS(f"✅ Generated {count} fake products at {output_path}")
#         )


# apps/accounts/management/commands/generate_products_json.py
import json
import uuid
import random
from pathlib import Path
from django.core.management.base import BaseCommand
from faker import Faker
from apps.accounts.models.user import User
from apps.products.models import (
    Category,
    Brand,
)  # ✅ assumes you have Category & Brand models

fake = Faker()


class Command(BaseCommand):
    help = "Generate fake products JSON file (auto-creates sellers, category, and brand if missing)"

    def add_arguments(self, parser):
        parser.add_argument("output_path", type=str, help="Where to save the JSON file")
        parser.add_argument(
            "--count", type=int, default=100, help="How many products to generate"
        )

    def handle(self, *args, **options):
        output_path = Path(options["output_path"])
        count = options["count"]

        # ✅ Ensure at least 5 sellers
        seller_ids = list(
            User.objects.filter(role="seller").values_list("id", flat=True)
        )
        if len(seller_ids) < 5:
            needed = 5 - len(seller_ids)
            self.stdout.write(
                self.style.WARNING(
                    f"⚠️ Only {len(seller_ids)} sellers found. Creating {needed} new sellers..."
                )
            )
            for _ in range(needed):
                user = User.objects.create_user(
                    email=fake.unique.email(),
                    username=fake.unique.user_name(),
                    password="password123",
                    role="seller",
                    is_email_verified=True,
                )
                seller_ids.append(user.id)

        # ✅ Ensure Default Category
        default_category, _ = Category.objects.get_or_create(
            name="Default Category",
            defaults={
                "slug": "default-category",
                "description": "Auto-created default category",
            },
        )

        # ✅ Ensure Default Brand
        default_brand, _ = Brand.objects.get_or_create(
            name="Default Brand",
            defaults={
                "slug": "default-brand",
                "description": "Auto-created default brand",
            },
        )

        # ✅ Now generate products
        products = []
        for _ in range(count):
            seller_id = random.choice(seller_ids)
            products.append(
                {
                    "id": str(uuid.uuid4()),
                    "title": fake.unique.sentence(nb_words=3).replace(".", ""),
                    "slug": fake.unique.slug(),
                    "description": fake.text(max_nb_chars=200),
                    "sku": fake.unique.ean(length=13),
                    "price": round(random.uniform(10, 500), 2),
                    "discount_price": (
                        round(random.uniform(5, 400), 2)
                        if random.choice([True, False])
                        else None
                    ),
                    "currency": "USD",
                    "stock": random.randint(1, 500),
                    "is_active": True,
                    "rating": round(random.uniform(1, 5), 1),
                    "review_count": random.randint(0, 1000),
                    "seller_id": str(seller_id),
                    "category_id": str(default_category.id),
                    "brand_id": str(default_brand.id),
                }
            )

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(products, f, indent=4)

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Generated {count} fake products at {output_path} "
                f"(sellers ensured: {len(seller_ids)}, category & brand ensured)"
            )
        )
