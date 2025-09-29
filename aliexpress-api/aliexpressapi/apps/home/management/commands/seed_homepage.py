# apps/home/management/commands/seed_homepage.py

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from apps.home.models.banner import HomepageBanner
from apps.home.models.section import HomepageSection
from apps.home.models.section_product import HomepageProduct
from apps.home.models.section_category import HomepageCategory
from apps.home.models.promotion import HomepagePromotion  # ✅ make sure this exists
from apps.products.models.category import Category
from apps.products.models.product import Product
from pathlib import Path


class Command(BaseCommand):
    help = "Seed homepage with demo sections, banners, featured products, categories, and promotions"

    def handle(self, *args, **kwargs):
        image_path = (
            Path(__file__).resolve().parent.parent.parent.parent.parent / "default.jpg"
        )
        if not image_path.exists():
            self.stdout.write(
                self.style.WARNING(f"⚠️ Default image not found: {image_path}")
            )
            return

        # 1️⃣ Create sections safely
        sections_data = [
            {"title": "Main Hero Banner", "type": "banner", "slug": "main-hero-banner"},
            {"title": "Flash Deals", "type": "products", "slug": "flash-deals"},
            {"title": "Top Categories", "type": "categories", "slug": "top-categories"},
            {"title": "Promotions", "type": "promo", "slug": "promo"},
        ]

        created_sections = []
        for data in sections_data:
            section, created = HomepageSection.objects.get_or_create(
                slug=data["slug"],
                defaults={
                    "title": data["title"],
                    "type": data["type"],
                    "is_active": True,
                },
            )
            if created:
                created_sections.append(section.title)
        self.stdout.write(
            self.style.SUCCESS(f"✅ Sections created: {created_sections}")
        )

        # Extract sections (always safe)
        hero_section = HomepageSection.objects.get(slug="main-hero-banner")
        flash_deals_section = HomepageSection.objects.get(slug="flash-deals")
        top_categories_section = HomepageSection.objects.get(slug="top-categories")
        promotions_section = HomepageSection.objects.get(slug="promo")

        # 2️⃣ Hero Banners
        hero_banners = [
            {"title": "Big Sale Banner", "link_url": "/sale"},
            {"title": "Sakku on Hero Image", "link_url": "/hero/sakku"},
        ]

        for banner_data in hero_banners:
            banner, created = HomepageBanner.objects.get_or_create(
                section=hero_section,
                title=banner_data["title"],
                defaults={"link_url": banner_data["link_url"]},
            )
            if created:
                with open(image_path, "rb") as img_file:
                    banner.image.save(
                        f"{banner.title.replace(' ', '_')}.jpg",
                        ContentFile(img_file.read()),
                        save=True,
                    )
        self.stdout.write(self.style.SUCCESS("✅ Banners seeded."))

        # 3️⃣ Flash Deal Products
        sample_products = Product.objects.all()[:5]
        for rank, product in enumerate(sample_products, start=1):
            if not product.image:
                with open(image_path, "rb") as img_file:
                    product.image.save(
                        f"{product.slug}.jpg", ContentFile(img_file.read()), save=True
                    )
            HomepageProduct.objects.get_or_create(
                section=flash_deals_section,
                product=product,
                defaults={"featured_rank": rank, "sort_order": rank},
            )
        self.stdout.write(self.style.SUCCESS("✅ Flash Deals seeded."))

        # 4️⃣ Top Categories
        top_categories = Category.objects.all()[:5]
        for order, category in enumerate(top_categories, start=1):
            HomepageCategory.objects.get_or_create(
                section=top_categories_section,
                category=category,
                defaults={"sort_order": order},
            )
        self.stdout.write(self.style.SUCCESS("✅ Top Categories seeded."))

        # 5️⃣ Promotions (A → E sample)
        promotions = [
            {"title": "Amazing Deal A", "link_url": "/promo/a"},
            {"title": "Brilliant Deal B", "link_url": "/promo/b"},
            {"title": "Cool Deal C", "link_url": "/promo/c"},
            {"title": "Discount D", "link_url": "/promo/d"},
            {"title": "Exclusive E", "link_url": "/promo/e"},
        ]

        for order, promo in enumerate(promotions, start=1):
            HomepagePromotion.objects.get_or_create(
                section=promotions_section,
                title=promo["title"],
                defaults={
                    "link_url": promo["link_url"],
                    "sort_order": order,
                },
            )
        self.stdout.write(self.style.SUCCESS("✅ Promotions seeded."))

        self.stdout.write(self.style.SUCCESS("🎉 Homepage seeded successfully!"))
