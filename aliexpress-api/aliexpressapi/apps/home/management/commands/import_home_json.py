import json
import uuid
from pathlib import Path
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.home.models.banner import HomepageBanner
from apps.home.models.section import HomepageSection
from apps.home.models.section_product import HomepageProduct
from apps.home.models.section_category import HomepageCategory
from apps.home.models.promotion import HomepagePromotion
from apps.products.models.category import Category
from apps.products.models.product import Product
from apps.products.models.brand import Brand
from apps.accounts.models.user import User


class Command(BaseCommand):
    help = "Import homepage JSON (sections, banners, products, categories, promotions)"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to JSON file")

    def handle(self, *args, **options):
        file_path = Path(options["file_path"])
        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f"❌ File not found: {file_path}"))
            return

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Default image
        default_image = (
            Path(__file__).parent.parent.parent.parent.parent / "default.jpg"
        )
        if not default_image.exists():
            self.stdout.write(
                self.style.WARNING(f"⚠️ Default image not found: {default_image}")
            )
            default_image = None

        # Default seller
        seller, _ = User.objects.get_or_create(
            email="default_seller@example.com",
            defaults={
                "username": "default_seller",
                "role": "seller",
                "is_active": True,
                "password": "test1234",
            },
        )

        # Default category and brand
        default_category, _ = Category.objects.get_or_create(
            name="Default Category", defaults={"slug": "default-category"}
        )
        default_brand, _ = Brand.objects.get_or_create(
            name="Default Brand", defaults={"slug": "default-brand"}
        )

        # Track existing slugs and SKUs to avoid duplicates
        existing_slugs = set(Product.objects.values_list("slug", flat=True))
        existing_skus = set(Product.objects.values_list("sku", flat=True))

        def unique_slug(title):
            base = slugify(title) or "product"
            slug = base
            counter = 1
            while slug in existing_slugs:
                slug = f"{base}-{counter}"
                counter += 1
            existing_slugs.add(slug)
            return slug

        def unique_sku(sku=None):
            sku = sku or f"sku-{uuid.uuid4().hex[:8]}"
            while sku in existing_skus:
                sku = f"sku-{uuid.uuid4().hex[:8]}"
            existing_skus.add(sku)
            return sku

        # Sections
        for sec in data.get("sections", []):
            HomepageSection.objects.get_or_create(
                slug=sec["slug"],
                defaults={
                    "title": sec["title"],
                    "type": sec["type"],
                    "is_active": True,
                },
            )

        sections_map = {s.slug: s for s in HomepageSection.objects.all()}

        # Banners
        for b in data.get("banners", []):
            section = sections_map.get(b["section_slug"])
            if not section:
                continue
            banner, _ = HomepageBanner.objects.get_or_create(
                section=section,
                title=b["title"],
                defaults={"link_url": b.get("link_url", "/")},
            )
            if default_image and not banner.image:
                with open(default_image, "rb") as f:
                    banner.image.save(
                        f"{b['title'].replace(' ', '_')}.jpg",
                        ContentFile(f.read()),
                        save=True,
                    )

        # Products
        for p in data.get("flash_deals", []):
            section = sections_map.get(p["section_slug"])
            if not section:
                continue
            slug = unique_slug(p.get("title", "product"))
            sku = unique_sku(p.get("sku"))

            product, _ = Product.objects.update_or_create(
                sku=sku,
                defaults={
                    "title": p.get("title", "Untitled Product"),
                    "slug": slug,
                    "description": p.get("description", ""),
                    "price": p.get("price", 0),
                    "discount_price": p.get("discount_price"),
                    "currency": p.get("currency", "USD"),
                    "stock": p.get("stock", 10),
                    "is_active": p.get("is_active", True),
                    "rating": p.get("rating", 0),
                    "review_count": p.get("review_count", 0),
                    "seller": seller,
                    "category": default_category,
                    "brand": default_brand,
                },
            )

            HomepageProduct.objects.get_or_create(
                section=section,
                product=product,
                defaults={
                    "featured_rank": p.get("featured_rank", 1),
                    "sort_order": p.get("sort_order", 1),
                },
            )

            if default_image and not product.image:
                with open(default_image, "rb") as f:
                    product.image.save(f"{slug}.jpg", ContentFile(f.read()), save=True)

        # Categories
        for c in data.get("categories", []):
            section = sections_map.get(c["section_slug"])
            if not section:
                continue
            cat_slug = slugify(c.get("name", "default-category"))
            category, _ = Category.objects.get_or_create(
                name=c.get("name", "Default Category"), defaults={"slug": cat_slug}
            )
            HomepageCategory.objects.get_or_create(
                section=section,
                category=category,
                defaults={"sort_order": c.get("sort_order", 1)},
            )

        # Promotions
        for promo in data.get("promotions", []):
            section = sections_map.get(promo["section_slug"])
            if not section:
                continue
            promo_obj, _ = HomepagePromotion.objects.get_or_create(
                section=section,
                title=promo["title"],
                defaults={"link_url": promo.get("link_url", "/")},
            )
            if default_image and not promo_obj.image:
                with open(default_image, "rb") as f:
                    promo_obj.image.save(
                        f"{promo['title'].replace(' ', '_')}.jpg",
                        ContentFile(f.read()),
                        save=True,
                    )

        self.stdout.write(
            self.style.SUCCESS(f"✅ Homepage imported successfully from {file_path}")
        )
