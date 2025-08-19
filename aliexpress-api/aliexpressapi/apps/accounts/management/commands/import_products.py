import json
import csv
from decimal import Decimal
from django.core.management.base import BaseCommand
from apps.products.models import Product, Category, Brand
from apps.accounts.models import User


class Command(BaseCommand):
    help = "Import products from a JSON or CSV file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to JSON or CSV file")
        parser.add_argument(
            "--format",
            type=str,
            choices=["json", "csv"],
            default="json",
            help="File format (json or csv)",
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]
        file_format = options["format"]

        try:
            if file_format == "json":
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:  # CSV
                with open(file_path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    data = list(reader)

            for item in data:
                self.create_product(item)

            self.stdout.write(self.style.SUCCESS("✅ Products imported successfully."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {e}"))

    def create_product(self, data):
        """
        Create or update a product from dict data
        """
        try:
            seller = User.objects.get(id=data["seller_id"])
            category = Category.objects.get(id=data["category_id"])
            brand = None
            if data.get("brand_id"):
                try:
                    brand = Brand.objects.get(id=data["brand_id"])
                except Brand.DoesNotExist:
                    brand = None

            Product.objects.update_or_create(
                sku=data["sku"],
                defaults={
                    "title": data["title"],
                    "slug": data["slug"],
                    "description": data.get("description", ""),
                    "price": Decimal(str(data["price"])),
                    "discount_price": (
                        Decimal(str(data["discount_price"]))
                        if data.get("discount_price")
                        else None
                    ),
                    "currency": data.get("currency", "USD"),
                    "stock": int(data.get("stock", 0)),
                    "is_active": (
                        bool(data.get("is_active"))
                        if str(data.get("is_active")).lower() not in ["false", "0", ""]
                        else False
                    ),
                    "rating": float(data.get("rating", 0.0)),
                    "review_count": int(data.get("review_count", 0)),
                    "seller": seller,
                    "category": category,
                    "brand": brand,
                },
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"❌ Failed to import product {data.get('title')}: {e}"
                )
            )
