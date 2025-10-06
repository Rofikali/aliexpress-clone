import json
import uuid
import random
from datetime import datetime, timezone
import factory
from factory import Faker as F, LazyFunction, Sequence

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.db import transaction

from apps.accounts.models import User
from apps.products.models.product import Product
from apps.products.models.brand import Brand
from apps.products.models.category import Category
from apps.products.models.inventory import Inventory
from apps.products.models.product_images import ProductImages
from apps.products.models.product_attribute import (
    ProductAttribute,
    ProductAttributeValue,
)
from apps.products.models.product_variant import ProductVariant, ProductVariantValue

from pathlib import Path

now = datetime.now(timezone.utc).isoformat()
img_path = (
    Path(__file__).resolve().parent.parent.parent.parent.parent
    / "media"
    / "default.jpg"
)


def new_uuid():
    return str(uuid.uuid4())


# --------------------------
# Factories
# --------------------------
class UserFactory(factory.Factory):
    class Meta:
        model = dict

    id = LazyFunction(new_uuid)
    email = F("email")
    username = F("user_name")
    password = "pbkdf2_sha256$..."
    role = factory.Iterator(["seller", "buyer"])
    is_active = True
    is_email_verified = True
    created_at = now
    updated_at = now


class CategoryFactory(factory.Factory):
    class Meta:
        model = dict

    id = LazyFunction(new_uuid)
    name = F("word")
    slug = F("slug")
    description = F("sentence")
    parent = None
    created_at = now
    updated_at = now


class BrandFactory(factory.Factory):
    class Meta:
        model = dict

    id = LazyFunction(new_uuid)
    name = F("company")
    slug = F("slug")
    description = F("sentence")
    logo = str(img_path)
    created_at = now
    updated_at = now


class ProductFactory(factory.Factory):
    class Meta:
        model = dict

    id = LazyFunction(new_uuid)
    title = F("sentence", nb_words=3)
    slug = F("slug")
    description = F("text", max_nb_chars=200)
    sku = F("ean13")
    price = LazyFunction(lambda: round(random.uniform(10, 500), 2))
    discount_price = None
    currency = "USD"
    stock = LazyFunction(lambda: random.randint(1, 500))
    is_active = True
    rating = LazyFunction(lambda: round(random.uniform(1, 5), 1))
    review_count = LazyFunction(lambda: random.randint(0, 1000))
    seller = None
    category = None
    brand = None
    image = str(img_path)
    created_at = now
    updated_at = now


class ProductImagesFactory(factory.Factory):
    class Meta:
        model = dict

    id = LazyFunction(new_uuid)
    product = None
    image = str(img_path)
    alt_text = F("sentence", nb_words=5)
    position = Sequence(lambda n: n)
    created_at = now
    updated_at = now


class ProductAttributeFactory(factory.Factory):
    class Meta:
        model = dict

    id = LazyFunction(new_uuid)
    name = Sequence(lambda n: f"Attribute {n}")
    sort_order = Sequence(lambda n: n)
    created_at = now
    updated_at = now


class ProductAttributeValueFactory(factory.Factory):
    class Meta:
        model = dict

    id = LazyFunction(new_uuid)
    attribute = None
    value = F("word")
    created_at = now
    updated_at = now


class ProductVariantFactory(factory.Factory):
    class Meta:
        model = dict

    id = LazyFunction(new_uuid)
    product = None
    sku = Sequence(lambda n: f"SKU-{n}-{random.randint(1000, 9999)}")
    price = LazyFunction(lambda: round(random.uniform(10, 500), 2))
    discount_price = None
    stock = LazyFunction(lambda: random.randint(1, 200))
    currency = "USD"
    image = None  # <- assign valid ProductImages UUID later
    is_active = True
    created_at = now
    updated_at = now


class ProductVariantValueFactory(factory.Factory):
    class Meta:
        model = dict

    id = LazyFunction(new_uuid)
    variant = None
    attribute = None
    value = None
    created_at = now
    updated_at = now


class InventoryFactory(factory.Factory):
    class Meta:
        model = dict

    id = LazyFunction(new_uuid)
    sku = None
    product = None
    stock = 0
    change = 0
    quantity = 0
    reason = "restock"
    location = "Main Warehouse"
    reference_id = LazyFunction(new_uuid)
    created_at = now


# --------------------------
# Fixture Generator
# --------------------------
def generate_product_fixture(filename="fixtures/products_fixture.json"):
    fixtures = []

    NUM_SELLERS = 10
    NUM_BUYERS = 10
    NUM_CATEGORIES = 50
    NUM_BRANDS = 10
    NUM_PRODUCTS = 30
    IMAGES_PER_PRODUCT = 3

    # Users
    sellers = [UserFactory(role="seller") for _ in range(NUM_SELLERS)]
    buyers = [UserFactory(role="buyer") for _ in range(NUM_BUYERS)]
    for u in sellers + buyers:
        fixtures.append({"model": "accounts.user", "pk": u["id"], "fields": u})

    # Categories
    categories = [CategoryFactory() for _ in range(NUM_CATEGORIES)]
    for c in categories:
        fixtures.append({"model": "products.category", "pk": c["id"], "fields": c})

    # Brands
    brands = [BrandFactory() for _ in range(NUM_BRANDS)]
    for b in brands:
        fixtures.append({"model": "products.brand", "pk": b["id"], "fields": b})

    # Products, Images, Variants
    attributes_def = {"Color": ["Red", "Blue", "Green"], "Size": ["S", "M", "L"]}
    attr_map = {}
    val_map = {}

    # Attributes & Values
    for idx, (name, vals) in enumerate(attributes_def.items(), start=1):
        attr = ProductAttributeFactory(name=name, sort_order=idx)
        attr_map[name] = attr["id"]
        fixtures.append(
            {"model": "products.productattribute", "pk": attr["id"], "fields": attr}
        )
        for v in vals:
            val = ProductAttributeValueFactory(attribute=attr["id"], value=v)
            val_map[(name, v)] = val["id"]
            fixtures.append(
                {
                    "model": "products.productattributevalue",
                    "pk": val["id"],
                    "fields": val,
                }
            )

    # Products
    for _ in range(NUM_PRODUCTS):
        p = ProductFactory(
            seller=random.choice(sellers)["id"],
            category=random.choice(categories)["id"],
            brand=random.choice(brands)["id"],
        )
        fixtures.append({"model": "products.product", "pk": p["id"], "fields": p})

        # Images
        p_images = []
        for i in range(IMAGES_PER_PRODUCT):
            img = ProductImagesFactory(product=p["id"], position=i)
            p_images.append(img)
            fixtures.append(
                {"model": "products.productimages", "pk": img["id"], "fields": img}
            )

        # Variants
        for _ in range(random.randint(1, 3)):
            variant = ProductVariantFactory(
                product=p["id"],
                image=p_images[0]["id"],  # <- valid UUID
            )
            fixtures.append(
                {
                    "model": "products.productvariant",
                    "pk": variant["id"],
                    "fields": variant,
                }
            )

            # Variant values
            for attr_name in random.sample(list(attributes_def.keys()), k=1):
                vname = random.choice(attributes_def[attr_name])
                vv = ProductVariantValueFactory(
                    variant=variant["id"],
                    attribute=attr_map[attr_name],
                    value=val_map[(attr_name, vname)],
                )
                fixtures.append(
                    {
                        "model": "products.productvariantvalue",
                        "pk": vv["id"],
                        "fields": vv,
                    }
                )

            # Inventory
            inv = InventoryFactory(
                sku=variant["sku"],
                product=p["id"],
                stock=variant["stock"],
                change=variant["stock"],
                quantity=variant["stock"],
            )
            fixtures.append(
                {"model": "products.inventory", "pk": inv["id"], "fields": inv}
            )

    # Save JSON
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(fixtures, f, indent=2)

    return fixtures


# --------------------------
# Management Command
# --------------------------
class Command(BaseCommand):
    help = "Generate product fixtures, clear old data, save to JSON, and load into DB"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="fixtures/products_fixture.json",
            help="Path to output fixture JSON file",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        filename = options["file"]

        self.stdout.write("🗑️  Clearing old product data...")
        Inventory.objects.all().delete()
        ProductVariantValue.objects.all().delete()
        ProductVariant.objects.all().delete()
        ProductAttributeValue.objects.all().delete()
        ProductAttribute.objects.all().delete()
        ProductImages.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Brand.objects.all().delete()
        User.objects.filter(role__in=["seller", "buyer"]).delete()
        self.stdout.write(self.style.SUCCESS("✅ Old product data cleared"))

        fixtures = generate_product_fixture(filename=filename)
        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Product fixture saved to {filename} ({len(fixtures)} records)"
            )
        )

        try:
            call_command("loaddata", filename)
            self.stdout.write(self.style.SUCCESS("✅ Fixture loaded into DB"))
        except Exception as e:
            raise CommandError(f"❌ Failed to load fixture: {e}")
