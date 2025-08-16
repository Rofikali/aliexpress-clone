from django.core.management.base import BaseCommand
from django.core.files import File
from apps.products.models import Products, ProductImages
from pathlib import Path


class Command(BaseCommand):
    help = "Generate exactly N product images per product (avoids duplicates)"

    def add_arguments(self, parser):
        parser.add_argument(
            "images_per_product",
            type=int,
            help="Total number of images each product should have",
        )

    def handle(self, *args, **kwargs):
        images_per_product = kwargs["images_per_product"]
        created = 0

        # Path to default image
        image_path = (
            Path(__file__).resolve().parent.parent.parent.parent.parent / "default.jpg"
        )

        if not image_path.exists():
            self.stdout.write(
                self.style.ERROR(f"Image file not found: {image_path}. Aborting.")
            )
            return

        products = Products.objects.all()
        if not products.exists():
            self.stdout.write(self.style.ERROR("No products found. Aborting."))
            return

        for product in products:
            existing_count = product.product_images.count()

            if existing_count >= images_per_product:
                self.stdout.write(
                    self.style.WARNING(
                        f"⚠️ {product.title} already has {existing_count} images (skipping)"
                    )
                )
                continue

            # Only create the difference
            to_create = images_per_product - existing_count

            for i in range(to_create):
                with open(image_path, "rb") as img_file:
                    django_file = File(
                        img_file,
                        name=f"{product.id}_{existing_count + i + 1}_{image_path.name}",
                    )

                    ProductImages.objects.create(
                        product_id=product, img_name=django_file
                    )
                    created += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✅ Added image {existing_count + i + 1} for product: {product.title}"
                        )
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 Done. {created} new images created (each product has max {images_per_product})."
            )
        )
