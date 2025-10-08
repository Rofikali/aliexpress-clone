# apps/home/management/commands/generate_homepage_fixtures.py
import json
import uuid
from datetime import datetime, timezone
from faker import Faker
import factory
from factory import Faker as F, LazyFunction, Sequence
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.db import transaction
from pathlib import Path

from apps.products.models.product import Product
from apps.products.models.category import Category
from apps.home.models.banner import HomepageBanner
from apps.home.models.promotion import HomepagePromotion
from apps.home.models.category import HomepageCategory
from apps.home.models.product import HomepageProduct

fake = Faker()
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
class HomepageBannerFactory(factory.Factory):
    class Meta:
        model = dict

    id = LazyFunction(new_uuid)
    title = F("sentence", nb_words=3)
    image = str(img_path)
    link_url = F("url")
    alt_text = F("sentence", nb_words=5)
    sort_order = Sequence(lambda n: n)
    is_active = True
    created_at = now
    updated_at = now


class HomepagePromotionFactory(factory.Factory):
    class Meta:
        model = dict

    id = LazyFunction(new_uuid)
    title = F("sentence", nb_words=3)
    description = F("sentence", nb_words=8)
    image = str(img_path)
    link_url = F("url")
    sort_order = Sequence(lambda n: n)
    is_active = True
    created_at = now
    updated_at = now


class HomepageCategoryFactory(factory.Factory):
    class Meta:
        model = dict

    id = LazyFunction(new_uuid)
    category_id = None
    sort_order = Sequence(lambda n: n)


class HomepageProductFactory(factory.Factory):
    class Meta:
        model = dict

    id = LazyFunction(new_uuid)
    product_id = None
    featured_rank = Sequence(lambda n: n + 1)
    sort_order = Sequence(lambda n: n)


# --------------------------
# Fixture generator
# --------------------------
def generate_homepage_fixture(filename="homepage_fixture.json"):
    fixtures = []

    # Banners
    for i in range(3):
        b = HomepageBannerFactory()
        fixtures.append(
            {
                "model": "home.homepagebanner",
                "pk": b["id"],
                "fields": {k: v for k, v in b.items() if k != "id"},
            }
        )

    # Promotions
    for i in range(3):
        p = HomepagePromotionFactory()
        fixtures.append(
            {
                "model": "home.homepagepromotion",
                "pk": p["id"],
                "fields": {k: v for k, v in p.items() if k != "id"},
            }
        )

    # Categories
    cats = list(Category.objects.values_list("id", flat=True)[:5])
    for idx, cat_id in enumerate(cats):
        c = HomepageCategoryFactory(category_id=str(cat_id), sort_order=idx)
        fixtures.append(
            {
                "model": "home.homepagecategory",
                "pk": c["id"],
                "fields": {k: v for k, v in c.items() if k != "id"},
            }
        )

    # Products
    prods = list(Product.objects.values_list("id", flat=True)[:5])
    for idx, prod_id in enumerate(prods):
        pr = HomepageProductFactory(
            product_id=str(prod_id), featured_rank=idx + 1, sort_order=idx
        )
        fixtures.append(
            {
                "model": "home.homepageproduct",
                "pk": pr["id"],
                "fields": {k: v for k, v in pr.items() if k != "id"},
            }
        )

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(fixtures, f, indent=2)

    return fixtures


# --------------------------
# Management Command
# --------------------------
class Command(BaseCommand):
    help = "Generate homepage fixtures, clear old data, save to JSON, and load into DB"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="fixtures/homepage_fixture.json",
            help="Path to output fixture JSON file",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        filename = options["file"]

        # 1. Clear old homepage data
        self.stdout.write("🗑️  Clearing old homepage data...")
        HomepageBanner.objects.all().delete()
        HomepagePromotion.objects.all().delete()
        HomepageCategory.objects.all().delete()
        HomepageProduct.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("✅ Old homepage data cleared"))

        # 2. Generate JSON fixture
        fixtures = generate_homepage_fixture(filename=filename)
        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Homepage fixture saved to {filename} ({len(fixtures)} records)"
            )
        )

        # 3. Load into DB
        try:
            call_command("loaddata", filename)
            self.stdout.write(self.style.SUCCESS("✅ Fixture loaded into DB"))
        except Exception as e:
            raise CommandError(f"❌ Failed to load fixture into DB: {e}")
