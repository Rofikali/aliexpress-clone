import json
import uuid
import random
from datetime import datetime, timezone
from faker import Faker

fake = Faker()
now = datetime.now(timezone.utc).isoformat()
image_path = "default.jpg"


def new_uuid():
    return str(uuid.uuid4())


class FixtureGenerator:
    def __init__(self):
        self.all_fixtures = []
        self.user_uuids = []
        self.category_uuids = []
        self.brand_uuids = []
        self.product_uuids = []
        self.product_index_to_uuid = {}
        self.product_image_uuids_per_product = {}
        self.attribute_uuid_map = {}
        self.value_uuid_map = {}
        self.product_variant_uuid_list = []

        # CONFIG
        self.NUM_SELLERS = 20
        self.NUM_BUYERS = 30
        self.NUM_USERS = self.NUM_SELLERS + self.NUM_BUYERS
        self.NUM_CATEGORIES = 30
        self.NUM_BRANDS = 30
        self.NUM_PRODUCTS = 200
        self.IMAGES_PER_PRODUCT = 3

    def generate_users(self):
        for i in range(self.NUM_USERS):
            u_id = new_uuid()
            self.user_uuids.append(u_id)
            self.all_fixtures.append(
                {
                    "model": "accounts.user",
                    "pk": u_id,
                    "fields": {
                        "id": u_id,
                        "email": fake.unique.email(),
                        "username": fake.unique.user_name(),
                        "password": "pbkdf2_sha256$...",
                        "role": "seller" if i < self.NUM_SELLERS else "buyer",
                        "is_active": True,
                        "is_email_verified": True,
                        "created_at": now,
                        "updated_at": now,
                    },
                }
            )

    def generate_categories(self):
        for _ in range(self.NUM_CATEGORIES):
            c_id = new_uuid()
            self.category_uuids.append(c_id)
            self.all_fixtures.append(
                {
                    "model": "products.category",
                    "pk": c_id,
                    "fields": {
                        "id": c_id,
                        "name": fake.unique.word().title(),
                        "slug": fake.unique.slug(),
                        "description": fake.text(max_nb_chars=100),
                        "parent": None,
                        "created_at": now,
                        "updated_at": now,
                    },
                }
            )

    def generate_brands(self):
        for _ in range(self.NUM_BRANDS):
            b_id = new_uuid()
            self.brand_uuids.append(b_id)
            self.all_fixtures.append(
                {
                    "model": "products.brand",
                    "pk": b_id,
                    "fields": {
                        "id": b_id,
                        "name": fake.unique.company(),
                        "slug": fake.unique.slug(),
                        "description": fake.text(max_nb_chars=100),
                        "logo": "",
                        "created_at": now,
                        "updated_at": now,
                    },
                }
            )

    def generate_products(self):
        for i in range(1, self.NUM_PRODUCTS + 1):
            p_id = new_uuid()
            self.product_uuids.append(p_id)
            self.product_index_to_uuid[i] = p_id
            self.all_fixtures.append(
                {
                    "model": "products.product",
                    "pk": p_id,
                    "fields": {
                        "id": p_id,
                        "title": fake.sentence(nb_words=3).replace(".", ""),
                        "slug": fake.unique.slug(),
                        "description": fake.text(max_nb_chars=200),
                        "sku": fake.unique.ean(length=13),
                        "price": round(random.uniform(10, 500), 2),
                        "discount_price": round(random.uniform(5, 400), 2)
                        if random.choice([True, False])
                        else None,
                        "currency": "USD",
                        "stock": random.randint(1, 500),
                        "is_active": True,
                        "rating": round(random.uniform(1, 5), 1),
                        "review_count": random.randint(0, 1000),
                        "seller": random.choice(self.user_uuids[: self.NUM_SELLERS]),
                        "category": random.choice(self.category_uuids),
                        "brand": random.choice(self.brand_uuids),
                        "image": image_path,
                        "created_at": now,
                        "updated_at": now,
                    },
                }
            )

    def generate_product_images(self):
        for idx in range(1, self.NUM_PRODUCTS + 1):
            prod_uuid = self.product_index_to_uuid[idx]
            self.product_image_uuids_per_product[prod_uuid] = []
            for pos in range(self.IMAGES_PER_PRODUCT):
                img_uuid = new_uuid()
                self.product_image_uuids_per_product[prod_uuid].append(img_uuid)
                self.all_fixtures.append(
                    {
                        "model": "products.productimages",
                        "pk": img_uuid,
                        "fields": {
                            "id": img_uuid,
                            "product": prod_uuid,
                            "image": image_path,
                            "alt_text": f"Image {pos + 1} for product {idx}",
                            "position": pos,
                            "created_at": now,
                            "updated_at": now,
                        },
                    }
                )

    def generate_attributes_and_values(self):
        attributes_def = [
            ("Color", ["Red", "Blue", "Green"]),
            ("Size", ["S", "M", "L"]),
            ("Material", ["Plastic", "Metal", "Textile"]),
            ("Warranty", ["None", "1 year", "2 years"]),
        ]
        for idx, (attr_name, vals) in enumerate(attributes_def, start=1):
            attr_uuid = new_uuid()
            self.attribute_uuid_map[attr_name] = attr_uuid
            self.all_fixtures.append(
                {
                    "model": "products.productattribute",
                    "pk": attr_uuid,
                    "fields": {
                        "id": attr_uuid,
                        "name": attr_name,
                        "sort_order": idx,
                        "created_at": now,
                        "updated_at": now,
                    },
                }
            )
            for v in vals:
                val_uuid = new_uuid()
                self.value_uuid_map[(attr_name, v)] = val_uuid
                self.all_fixtures.append(
                    {
                        "model": "products.productattributevalue",
                        "pk": val_uuid,
                        "fields": {
                            "id": val_uuid,
                            "attribute": attr_uuid,
                            "value": v,
                            "created_at": now,
                            "updated_at": now,
                        },
                    }
                )

    def generate_product_variants_and_values(self):
        for idx in range(1, self.NUM_PRODUCTS + 1):
            prod_uuid = self.product_index_to_uuid[idx]
            num_variants = random.randint(1, 3)
            for v in range(num_variants):
                var_uuid = new_uuid()
                self.product_variant_uuid_list.append(var_uuid)
                self.all_fixtures.append(
                    {
                        "model": "products.productvariant",
                        "pk": var_uuid,
                        "fields": {
                            "id": var_uuid,
                            "product": prod_uuid,
                            "sku": f"{idx}-{v + 1}-{random.randint(1000, 9999)}",
                            "price": round(random.uniform(10, 500), 2),
                            "discount_price": round(random.uniform(5, 400), 2)
                            if random.choice([True, False])
                            else None,
                            "stock": random.randint(1, 200),
                            "currency": "USD",
                            "image": self.product_image_uuids_per_product[prod_uuid][0],
                            "is_active": True,
                            "created_at": now,
                            "updated_at": now,
                        },
                    }
                )

                # Assign 1-2 unique attribute values
                num_attrs = random.randint(1, 2)
                chosen_attrs = random.sample(
                    list(self.attribute_uuid_map.keys()), k=num_attrs
                )
                for attr_name in chosen_attrs:
                    val = random.choice(
                        [v for v in dict(self.value_uuid_map) if v[0] == attr_name]
                    )[1]
                    val_uuid = self.value_uuid_map[(attr_name, val)]
                    self.all_fixtures.append(
                        {
                            "model": "products.productvariantvalue",
                            "pk": new_uuid(),
                            "fields": {
                                "id": new_uuid(),
                                "variant": var_uuid,
                                "attribute": self.attribute_uuid_map[attr_name],
                                "value": val_uuid,
                                "created_at": now,
                                "updated_at": now,
                            },
                        }
                    )

    def generate_inventory(self):
        for var_uuid in self.product_variant_uuid_list:
            # Get product variant info from previous fixture
            variant = next(
                (
                    f
                    for f in self.all_fixtures
                    if f["pk"] == var_uuid and f["model"] == "products.productvariant"
                ),
                None,
            )
            if variant:
                prod_uuid = variant["fields"]["product"]
                stock = variant["fields"]["stock"]
                sku = variant["fields"]["sku"]
                # create an inventory record
                self.all_fixtures.append(
                    {
                        "model": "products.inventory",
                        "pk": new_uuid(),
                        "fields": {
                            "id": new_uuid(),
                            "sku": sku,
                            "product": prod_uuid,
                            "stock": stock,
                            "change": stock,  # initial stock
                            "quantity": stock,
                            "reason": "restock",
                            "location": "Main Warehouse",
                            "reference_id": new_uuid(),
                            "created_at": now,
                        },
                    }
                )

    def save_fixture(self, filename="full_fixture.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.all_fixtures, f, indent=2)
        print(
            f"✅ {filename} generated — ready for `python manage.py loaddata {filename}`"
        )

    def generate_all(self):
        self.generate_users()
        self.generate_categories()
        self.generate_brands()
        self.generate_products()
        self.generate_product_images()
        self.generate_attributes_and_values()
        self.generate_product_variants_and_values()
        self.generate_inventory()  # ✅ Add inventory
        self.save_fixture()


if __name__ == "__main__":
    FixtureGenerator().generate_all()
