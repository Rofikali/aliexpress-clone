# # apps/accounts/management/commands/gererate_products_json.py
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
#                     "sku": fake.unique.ean(length=13),  # random SKU
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
#                     # 👉 IDs must match existing DB records
#                     "seller_id": 1,  # replace with a valid User.id
#                     "category_id": 1,  # replace with a valid Category.id
#                     "brand_id": None,  # or a valid Brand.id
#                 }
#             )

#         with open(output_path, "w", encoding="utf-8") as f:
#             json.dump(products, f, indent=4)

#         self.stdout.write(
#             self.style.SUCCESS(f"✅ Generated {count} fake products at {output_path}")
#         )
import json
import uuid
import random
from pathlib import Path
from django.core.management.base import BaseCommand
from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = "Generate fake products JSON file"

    def add_arguments(self, parser):
        parser.add_argument("output_path", type=str, help="Where to save the JSON file")
        parser.add_argument(
            "--count", type=int, default=100, help="How many products to generate"
        )

    def handle(self, *args, **options):
        output_path = Path(options["output_path"])
        count = options["count"]

        products = []
        for i in range(count):
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
                    "seller_id": 1,  # valid User.id
                    "category_id": None,  # let import assign Default Category
                    "brand_id": None,  # let import assign Default Brand
                }
            )

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(products, f, indent=4)

        self.stdout.write(
            self.style.SUCCESS(f"✅ Generated {count} fake products at {output_path}")
        )
