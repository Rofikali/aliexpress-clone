# # apps/accounts/management/commands/import_products.py
# import json
# import csv
# from decimal import Decimal
# from pathlib import Path
# from django.core.files.base import ContentFile
# from django.core.management.base import BaseCommand
# from apps.products.models import Product, Category, Brand, ProductImage  # 👈 added ProductImage
# from apps.accounts.models import User


# class Command(BaseCommand):
#     help = "Import products from a JSON or CSV file"

#     def add_arguments(self, parser):
#         parser.add_argument("file_path", type=str, help="Path to JSON or CSV file")
#         parser.add_argument(
#             "--format",
#             type=str,
#             choices=["json", "csv"],
#             default="json",
#             help="File format (json or csv)",
#         )

#     def handle(self, *args, **options):
#         file_path = options["file_path"]
#         file_format = options["format"]

#         try:
#             if file_format == "json":
#                 with open(file_path, "r", encoding="utf-8") as f:
#                     data = json.load(f)
#             else:  # CSV
#                 with open(file_path, "r", encoding="utf-8") as f:
#                     reader = csv.DictReader(f)
#                     data = list(reader)

#             for item in data:
#                 self.create_product(item)

#             self.stdout.write(self.style.SUCCESS("✅ Products imported successfully."))

#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f"❌ Error: {e}"))

#     def create_product(self, data):
#         """
#         Create or update a product with 1 main image + 5 stock gallery images
#         """
#         try:
#             seller = User.objects.get(id=data["seller_id"])
#             category = Category.objects.get(id=data["category_id"])
#             brand = None
#             if data.get("brand_id"):
#                 try:
#                     brand = Brand.objects.get(id=data["brand_id"])
#                 except Brand.DoesNotExist:
#                     brand = None

#             product, _ = Product.objects.update_or_create(
#                 sku=data["sku"],
#                 defaults={
#                     "title": data["title"],
#                     "slug": data["slug"],
#                     "description": data.get("description", ""),
#                     "price": Decimal(str(data["price"])),
#                     "discount_price": (
#                         Decimal(str(data["discount_price"]))
#                         if data.get("discount_price")
#                         else None
#                     ),
#                     "currency": data.get("currency", "USD"),
#                     "stock": int(data.get("stock", 0)),
#                     "is_active": (
#                         bool(data.get("is_active"))
#                         if str(data.get("is_active")).lower() not in ["false", "0", ""]
#                         else False
#                     ),
#                     "rating": float(data.get("rating", 0.0)),
#                     "review_count": int(data.get("review_count", 0)),
#                     "seller": seller,
#                     "category": category,
#                     "brand": brand,
#                 },
#             )

#             # ✅ Use same stock image for all products
#             image_path = Path(__file__).resolve().parent.parent.parent.parent.parent / "default.jpg"
#             # print('image path ', image_path)
#             if not image_path.exists():
#                 self.stdout.write(self.style.WARNING(f"⚠️ Default image not found: {image_path}"))
#                 return

#             # -- 1 main image (Product.image) --
#             with open(image_path, "rb") as img_file:
#                 product.image.save(f"{product.slug}.jpg", ContentFile(img_file.read()), save=True)

#             # -- 5 stock gallery images (ProductImage) --
#             ProductImage.objects.filter(product=product).delete()  # clear old
#             with open(image_path, "rb") as img_file:
#                 image_bytes = img_file.read()
#                 for i in range(5):
#                     ProductImage.objects.create(
#                         product=product,
#                         image=ContentFile(image_bytes, name=f"{product.slug}-{i+1}.jpg"),
#                     )

#         except Exception as e:
#             self.stdout.write(
#                 self.style.ERROR(f"❌ Failed to import product {data.get('title')}: {e}")
#             )
import json
import csv
from decimal import Decimal
from pathlib import Path
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from apps.products.models import Product, Category, Brand, ProductImage
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
        Create or update a product with 1 main image + 5 stock gallery images
        """
        try:
            seller = User.objects.get(id=data["seller_id"])

            # ✅ Ensure default category
            category = None
            try:
                if data.get("category_id"):
                    category = Category.objects.get(id=data["category_id"])
            except Category.DoesNotExist:
                category = None
            if not category:
                category, _ = Category.objects.get_or_create(name="Default Category")

            # ✅ Ensure default brand
            brand = None
            try:
                if data.get("brand_id"):
                    brand = Brand.objects.get(id=data["brand_id"])
            except Brand.DoesNotExist:
                brand = None
            if not brand:
                brand, _ = Brand.objects.get_or_create(name="Default Brand")

            product, _ = Product.objects.update_or_create(
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

            # ✅ Use same stock image for all products
            image_path = (
                Path(__file__).resolve().parent.parent.parent.parent.parent
                / "default.jpg"
            )
            if not image_path.exists():
                self.stdout.write(
                    self.style.WARNING(f"⚠️ Default image not found: {image_path}")
                )
                return

            # -- 1 main image (Product.image) --
            with open(image_path, "rb") as img_file:
                product.image.save(
                    f"{product.slug}.jpg", ContentFile(img_file.read()), save=True
                )

            # -- 5 stock gallery images (ProductImage) --
            ProductImage.objects.filter(product=product).delete()
            with open(image_path, "rb") as img_file:
                image_bytes = img_file.read()
                for i in range(5):
                    ProductImage.objects.create(
                        product=product,
                        image=ContentFile(
                            image_bytes, name=f"{product.slug}-{i + 1}.jpg"
                        ),
                    )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f"❌ Failed to import product {data.get('title')}: {e}"
                )
            )
