# from django.core.management.base import BaseCommand
# from apps.home.models.banner import HomepageBanner
# from apps.home.models.section import HomepageSection
# from apps.home.models.section_product import HomepageProduct
# from apps.products.models.category import Category
# from apps.products.models.product import Product
# from pathlib import Path


# class Command(BaseCommand):
#     help = "Seed homepage with demo sections, banners, and featured products"

#     def handle(self, *args, **kwargs):
#         # 1️⃣ Create sections
#         hero_section, _ = HomepageSection.objects.get_or_create(
#             title="Main Hero Banner",
#             type="banner",
#             defaults={
#                 "is_active": True,
#             },
#         )

#         flash_deals, _ = HomepageSection.objects.get_or_create(
#             title="Flash Deals",
#             type="products",
#             defaults={
#                 "is_active": True,
#             },
#         )

#         categories, _ = HomepageSection.objects.get_or_create(
#             title="Top Categories",
#             type="categories",
#             defaults={"is_active": True},
#         )

#         self.stdout.write(self.style.SUCCESS("✅ Sections created."))
#         # ✅ Use same stock image for all products
#         image_path = (
#             Path(__file__).resolve().parent.parent.parent.parent.parent / "default.jpg"
#         )

#         # 2️⃣ Create banner
#         HomepageBanner.objects.get_or_create(
#             section=hero_section,
#             title="Big Sale Banner",
#             defaults={
#                 "image": image_path,
#                 "link_url": "/sale",
#             },
#         )
#         self.stdout.write(self.style.SUCCESS("✅ Banner created."))

#         # 3️⃣ Attach products (first 5 as Flash Deals)
#         sample_products = Product.objects.all()[:5]
#         for rank, product in enumerate(sample_products, start=1):
#             HomepageProduct.objects.get_or_create(
#                 section=flash_deals,
#                 product=product,
#                 defaults={"featured_rank": rank},
#             )
#         self.stdout.write(self.style.SUCCESS("✅ Flash Deal products linked."))

#         self.stdout.write(self.style.SUCCESS("🎉 Homepage seeded successfully!"))


from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from apps.home.models.banner import HomepageBanner
from apps.home.models.section import HomepageSection
from apps.home.models.section_product import HomepageProduct
from apps.home.models.section_category import HomepageCategory
from apps.products.models.category import Category
from apps.products.models.product import Product
from pathlib import Path


class Command(BaseCommand):
    help = (
        "Seed homepage with demo sections, banners, featured products, and categories"
    )

    def handle(self, *args, **kwargs):
        image_path = (
            Path(__file__).resolve().parent.parent.parent.parent.parent / "default.jpg"
        )
        if not image_path.exists():
            self.stdout.write(
                self.style.WARNING(f"⚠️ Default image not found: {image_path}")
            )
            return

        # 1️⃣ Create sections
        sections_data = [
            {"title": "Main Hero Banner", "type": "banner", "slug": "main-hero-banner"},
            {"title": "Flash Deals", "type": "products", "slug": "flash-deals"},
            {"title": "Top Categories", "type": "categories", "slug": "top-categories"},
        ]

        created_sections = []
        for data in sections_data:
            section, created = HomepageSection.objects.get_or_create(
                title=data["title"],
                type=data["type"],
                defaults={"is_active": True, "slug": data["slug"]},
            )
            if created:
                created_sections.append(section.title)
        self.stdout.write(
            self.style.SUCCESS(f"✅ Sections created: {created_sections}")
        )

        # Extract sections
        hero_section = HomepageSection.objects.get(slug="main-hero-banner")
        flash_deals_section = HomepageSection.objects.get(slug="flash-deals")
        top_categories_section = HomepageSection.objects.get(slug="top-categories")

        # 2️⃣ Create hero banners
        hero_banners = [
            {"title": "Big Sale Banner", "link_url": "/sale"},
            {"title": "Sakku on Hero Image", "link_url": "/hero/sakku"},
        ]

        created_banners = []
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
                created_banners.append(banner.title)
        self.stdout.write(self.style.SUCCESS(f"✅ Banners created: {created_banners}"))

        # 3️⃣ Attach products to Flash Deals
        sample_products = Product.objects.all()[:5]
        created_products = []
        for rank, product in enumerate(sample_products, start=1):
            if not product.image:
                with open(image_path, "rb") as img_file:
                    product.image.save(
                        f"{product.slug}.jpg", ContentFile(img_file.read()), save=True
                    )
            hp, created = HomepageProduct.objects.get_or_create(
                section=flash_deals_section,
                product=product,
                defaults={"featured_rank": rank, "sort_order": rank},
            )
            if created:
                created_products.append(product.title)
        self.stdout.write(
            self.style.SUCCESS(f"✅ Flash Deal products linked: {created_products}")
        )

        # 4️⃣ Attach top categories
        top_categories = Category.objects.all()[:5]
        created_categories = []
        for order, category in enumerate(top_categories, start=1):
            hc, created = HomepageCategory.objects.get_or_create(
                section=top_categories_section,
                category=category,
                defaults={"sort_order": order},
            )
            if created:
                created_categories.append(category.name)
        self.stdout.write(
            self.style.SUCCESS(f"✅ Top categories linked: {created_categories}")
        )

        self.stdout.write(self.style.SUCCESS("🎉 Homepage seeded successfully!"))
