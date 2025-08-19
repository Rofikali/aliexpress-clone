import json
import uuid
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from faker import Faker
from apps.accounts.models import User
from apps.products.models import Category, Brand


class Command(BaseCommand):
    help = "Generate fake products and save them to a JSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            type=str,
            help="Output JSON file path (e.g., ./data/fake_products.json)",
        )
        parser.add_argument(
            "--count", type=int, default=100, help="Number of products to generate"
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]
        count = options["count"]

        fake = Faker()
        users = list(User.objects.all())
        categories = list(Category.objects.all())
        brands = list(Brand.objects.all())

        if not users or not categories:
            self.stdout.write(
                self.style.ERROR("Need at least 1 User and 1 Category in DB")
            )
            return

        data = []
        for _ in range(count):
            title = fake.unique.sentence(nb_words=3).replace(".", "")
            slug = "-".join(title.lower().split())
            price = round(random.uniform(10, 2000), 2)
            discount_price = (
                round(price * random.uniform(0.5, 0.9), 2)
                if random.choice([True, False])
                else None
            )

            product = {
                "id": str(uuid.uuid4()),
                "title": title,
                "slug": slug,
                "description": fake.text(max_nb_chars=200),
                "sku": fake.unique.bothify("SKU-####-????"),
                "price": str(price),
                "discount_price": str(discount_price) if discount_price else None,
                "currency": "USD",
                "stock": random.randint(0, 500),
                "is_active": random.choice([True, True, False]),
                "rating": round(random.uniform(1.0, 5.0), 1),
                "review_count": random.randint(0, 200),
                "seller_id": random.choice(users).id,
                "category_id": random.choice(categories).id,
                "brand_id": random.choice(brands).id if brands else None,
            }
            data.append(product)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        self.stdout.write(
            self.style.SUCCESS(f"{count} fake products saved to {file_path}")
        )
