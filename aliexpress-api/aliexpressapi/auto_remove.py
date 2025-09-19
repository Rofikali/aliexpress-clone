# aliexpress-api/aliexpressapi/auto_remove.py
from pathlib import Path
import shutil
import django
import os
from django.core.management import call_command


class Cleaner:
    """Base cleaner with common helpers."""

    def __init__(self, path: Path):
        self.path = path

    def exists(self) -> bool:
        return self.path.exists()


class DatabaseCleaner(Cleaner):
    """Removes a database file like db.sqlite3."""

    def clean(self):
        if not self.exists():
            print("No SQLite file found")
            return

        if self.path.is_file():
            print(f"Removing SQLite file: {self.path}")
            self.path.unlink()
        else:
            print(f"{self.path} exists but is not a file, skipping...")


class PycacheCleaner(Cleaner):
    """Removes all __pycache__ directories under a base path."""

    def clean(self):
        if not self.exists() or not self.path.is_dir():
            print("Apps dir does not exist")
            return

        print("Apps dir exists")
        removed = False
        for path in self.path.rglob("*"):
            if "__pycache__" in path.parts and path.is_dir():
                print(f"Removing pycache dir: {path}")
                shutil.rmtree(path)
                removed = True

        if not removed:
            print("No __pycache__ directories found")


class MigrationsCleaner(Cleaner):
    """
    Removes all migration files under a base path except __init__.py.

    - Keeps the __init__.py file (so the migrations folder remains a valid package).
    - Prints messages as it cleans.
    """

    def clean(self):
        if not self.exists() or not self.path.is_dir():
            print("Apps dir does not exist")
            return

        print("Apps dir exists")
        removed = False

        for path in self.path.rglob("migrations"):
            if path.is_dir():
                for file in path.iterdir():
                    if file.suffix == ".py":
                        if file.name == "__init__.py":
                            print(f"Keeping __init__.py in: {path}")
                        else:
                            print(f"Removing migration file: {file}")
                            file.unlink()
                            removed = True

        if not removed:
            print("No migration files found")


class ProductsCommandRunner:
    """Runs custom management commands for products."""

    def __init__(self, json_path: str):
        self.json_path = json_path

    def run(self):
        from django.core.management import CommandError

        try:
            print("✅ Running generate_products_json...")
            call_command("generate_products_json", self.json_path, count=50)
        except CommandError as e:
            print(f"❌ Error in generate_products_json: {e}")

        try:
            print("✅ Running import_products...")
            call_command("import_products", self.json_path, format="json")
        except CommandError as e:
            print(f"❌ Error in import_products: {e}")


# class LoadProducts:
#     def __init__(self):
#         pass

#     def __call__(self, *args, **kwds):
#         setup.call_command("loaddata", "fake_products.json")


# --- usage ---
if __name__ == "__main__":
    # Set up Django so call_command works
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings.dev")
    django.setup()

    base = Path("./apps")
    db_file = Path("./database/db.sqlite3")

    # DatabaseCleaner(db_file).clean()
    # PycacheCleaner(base).clean()
    # MigrationsCleaner(base).clean()

    # ✅ Call custom Django management commands
    ProductsCommandRunner("./apps/accounts/management/fake_products.json").run()
