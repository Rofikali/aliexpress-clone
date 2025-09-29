#  apps/home/management/commands/generate_home_json.py
import json
import uuid
from pathlib import Path
from django.core.management.base import BaseCommand
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Generate fake homepage JSON data (10 products and 10 promotions) without touching DB"

    def add_arguments(self, parser):
        parser.add_argument("output_path", type=str, help="Path to save the JSON file")

    def handle(self, *args, **options):
        output_path = Path(options["output_path"])

        # Sections
        sections = [
            {
                "id": str(uuid.uuid4()),
                "title": "Main Hero Banner",
                "slug": "main-hero-banner",
                "type": "banner",
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Flash Deals",
                "slug": "flash-deals",
                "type": "products",
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Top Categories",
                "slug": "top-categories",
                "type": "categories",
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Promotions",
                "slug": "promo",
                "type": "promo",
            },
        ]

        # Banners
        banners = [
            {
                "id": str(uuid.uuid4()),
                "section_slug": "main-hero-banner",
                "title": "Big Sale Banner",
                "link_url": "/sale",
                "image": "default.jpg",
            },
            {
                "id": str(uuid.uuid4()),
                "section_slug": "main-hero-banner",
                "title": "Sakku on Hero Image",
                "link_url": "/hero/sakku",
                "image": "default.jpg",
            },
        ]

        # Flash Deals: 10 products
        flash_deals = []
        for i in range(1, 11):
            flash_deals.append(
                {
                    "id": str(uuid.uuid4()),
                    "section_slug": "flash-deals",
                    "title": f"Product {i}",
                    "slug": f"product-{i}",
                    "description": f"Sample description for Product {i}",
                    "price": 100 + i * 5,
                    "sku": f"sku-{uuid.uuid4().hex[:8]}",
                    "image": "default.jpg",
                }
            )

        # Categories: 10 categories
        categories = []
        for i in range(1, 11):
            categories.append(
                {
                    "id": str(uuid.uuid4()),
                    "section_slug": "top-categories",
                    "name": f"Category {i}",
                    "slug": f"category-{i}",
                    "image": "default.jpg",
                }
            )

        # Promotions: 10 promotions
        promotions = []
        for i in range(1, 11):
            promotions.append(
                {
                    "id": str(uuid.uuid4()),
                    "section_slug": "promo",
                    "title": f"Promotion {i}",
                    "link_url": f"/promo/{i}",
                    "image": "default.jpg",
                }
            )

        # Combine all
        data = {
            "sections": sections,
            "banners": banners,
            "flash_deals": flash_deals,
            "categories": categories,
            "promotions": promotions,
        }

        # Write to file
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        self.stdout.write(
            self.style.SUCCESS(f"✅ Homepage JSON generated at {output_path}")
        )
