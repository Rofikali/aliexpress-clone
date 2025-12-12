import os
import sys
import subprocess
import shutil
import django
import time
from pathlib import Path
from threading import Thread
from django.db import connections


# ======================================================
# Spinner
# ======================================================
class Spinner:
    def __init__(self, message="Processing..."):
        self.message = message
        self.running = False
        self.spinner_cycle = ["|", "/", "-", "\\"]

    def start(self):
        self.running = True
        Thread(target=self._spin, daemon=True).start()

    def _spin(self):
        idx = 0
        while self.running:
            print(
                f"\r{self.message} {self.spinner_cycle[idx % len(self.spinner_cycle)]}",
                end="",
            )
            idx += 1
            time.sleep(0.08)

    def stop(self):
        self.running = False
        print("\r", end="")


# ======================================================
# Timer
# ======================================================
class Timer:
    def __init__(self, label="Elapsed"):
        self.label = label
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        if self.start_time is None:
            print("⚠️ Timer not started.")
            return None
        elapsed = time.time() - self.start_time
        print(f"⏱️ {self.label}: {elapsed:.2f} seconds")
        return elapsed


# ======================================================
# Helpers
# ======================================================
def run_cmd(cmd, show_spinner=False, message=None):
    if show_spinner and message:
        spinner = Spinner(message)
        spinner.start()
        result = subprocess.run(cmd, shell=True)
        spinner.stop()
    else:
        result = subprocess.run(cmd, shell=True)

    if result.returncode != 0:
        print(f"❌ Command failed: {cmd}")
        sys.exit(result.returncode)


def ensure_dir(path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created folder: {path}")


# ======================================================
# Cleaners
# ======================================================
class Cleaner:
    def __init__(self, path: Path):
        self.path = path

    def exists(self) -> bool:
        return self.path.exists()


class DatabaseCleaner(Cleaner):
    def __init__(self, path: Path, retries: int = 6, delay: float = 0.6):
        super().__init__(path)
        self.retries = retries
        self.delay = delay

    def clean(self):
        if not self.exists():
            print("No DB file found")
            return

        try:
            connections.close_all()
        except:
            pass

        spinner = Spinner(f"Deleting DB: {self.path}")
        spinner.start()

        for _ in range(self.retries):
            try:
                self.path.unlink()
                spinner.stop()
                print("🗑️ Database deleted")
                return
            except:
                time.sleep(self.delay)

        spinner.stop()
        print("❌ Database could not be deleted. Close apps using DB.")
        raise PermissionError("File locked!")


class PycacheCleaner(Cleaner):
    def clean(self):
        for p in self.path.rglob("__pycache__"):
            if p.is_dir():
                shutil.rmtree(p)
                print("🧹 Removed:", p)


class MigrationsCleaner(Cleaner):
    def clean(self):
        for m in self.path.rglob("migrations"):
            for f in list(m.iterdir()):
                if f.is_file() and f.name != "__init__.py":
                    f.unlink()
                    print("🧹 Removed:", f)


# ======================================================
# Migration + Superuser
# ======================================================
class MigrationAndSuperuser:
    def run(self):
        run_cmd(
            "uv run manage.py makemigrations",
            show_spinner=True,
            message="Making migrations",
        )
        run_cmd(
            "uv run manage.py migrate", show_spinner=True, message="Applying migrations"
        )

        print("Checking superuser...")
        django.setup()
        from apps.accounts.models import User

        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username="admin", email="admin@gmail.com", password="admin"
            )
            print("👑 Superuser created")
        else:
            print("✔️ Superuser already exists")


# ======================================================
# Fixture Loader
# ======================================================
class FixtureLoader:
    def __init__(self, fixture_path, retries=3, delay=1.5):
        self.fixture_path = fixture_path
        self.retries = retries
        self.delay = delay

    def load(self):
        attempt = 1
        while attempt <= self.retries:
            result = subprocess.run(
                f"python manage.py loaddata {self.fixture_path}", shell=True
            )
            if result.returncode == 0:
                print("📦 Fixtures loaded successfully")
                return
            time.sleep(self.delay)
            attempt += 1
        print("❌ Failed loading fixtures")


def autodetect_django_settings():
    """
    Detect Django settings automatically based on this structure:

        aliexpress-api/
        ├── Menu.py
        └── aliexpressapi/
            └── configs/settings/dev.py
    """

    # Folder containing Menu.py → aliexpress-api
    project_root = Path(__file__).resolve().parent

    # Django project folder → aliexpressapi
    django_root = project_root / "aliexpressapi"

    # Full path to dev.py
    settings_file = django_root / "configs" / "settings" / "dev.py"

    if not settings_file.exists():
        raise RuntimeError(f"❌ Could not locate Django dev.py at: {settings_file}")

    # Convert path to module string
    # aliexpressapi/configs/settings/dev.py → configs.settings.dev
    relative_path = settings_file.relative_to(django_root)
    module_name = ".".join(relative_path.with_suffix("").parts)

    # Make Django importable
    sys.path.insert(0, str(django_root))

    os.environ["DJANGO_SETTINGS_MODULE"] = module_name
    print(f"📌 Using Django settings: {module_name}")


# ======================================================
# NEW CLASS: GenerateFixtures
# ======================================================
class GenerateFixtures:
    """Reusable fixture generator class for future projects."""

    def run(self):
        print("🔄 Generating fixtures...")
        run_cmd("uv run manage.py generate_fixtures")
        run_cmd("uv run manage.py generate_homepage_fixtures")
        print("✨ Fixture generation completed!")


# ======================================================
# MENU
# ======================================================
def menu():
    print("\n=== Automation Menu ===")
    print("1️⃣ Remove DB")
    print("2️⃣ Remove __pycache__")
    print("3️⃣ Remove migration files")
    print("4️⃣ Run migrations + Ensure Superuser")
    print("5️⃣ Load Products Fixture")
    print("6️⃣ FULL RESET (DB + Pycache + Migrations + Migrate)")
    print("7️⃣ Generate Fixtures (NEW)")
    print("0️⃣ Exit")
    return input("Choose: ").strip()


# ======================================================
# Auto-Detect Django Settings (Path-based)
# ======================================================
# def autodetect_django_settings():
#     """
#     Automatically locates the Django settings module based on your
#     folder structure:
#         aliexpress-api/aliexpressapi/configs/settings/dev.py
#     """
#     root = Path(__file__).resolve().parent
#     print(f"🔍 Detecting Django settings from root: {root}")

#     # Your Django project root (contains manage.py)
#     # Modify if needed:
#     api_root = root / "aliexpress-api" / "aliexpressapi"

#     settings_file = api_root / "configs" / "settings" / "dev.py"

#     if not settings_file.exists():
#         raise RuntimeError(f"❌ Could not locate Django dev.py at: {settings_file}")

#     # Convert path → module string
#     # aliexpressapi/configs/settings/dev.py → "configs.settings.dev"
#     relative_path = settings_file.relative_to(api_root)
#     module_parts = list(relative_path.with_suffix("").parts)
#     settings_module = ".".join(module_parts)

#     # Ensure Django can import this
#     sys.path.insert(0, str(api_root))

#     os.environ["DJANGO_SETTINGS_MODULE"] = settings_module
#     print(f"📌 Using Django settings: {settings_module}")


# Call the auto-detector BEFORE django.setup()
# autodetect_django_settings()


# ======================================================
# MAIN LOOP
# ======================================================
if __name__ == "__main__":
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings.dev")
    autodetect_django_settings()
    django.setup()

    # apps_path = Path("./apps")
    # db_file = Path("./database/db.sqlite3")

    apps_path = Path("./apps")
    db_folder = Path("./database")
    db_file = db_folder / "db.sqlite3"
    fixtures_folder = Path("./fixtures")

    # Ensure required folders exist
    ensure_dir(apps_path)
    ensure_dir(db_folder)
    ensure_dir(fixtures_folder)

    while True:
        choice = menu()

        if choice == "1":
            DatabaseCleaner(db_file).clean()

        elif choice == "2":
            PycacheCleaner(apps_path).clean()

        elif choice == "3":
            MigrationsCleaner(apps_path).clean()

        elif choice == "4":
            MigrationAndSuperuser().run()

        elif choice == "5":
            FixtureLoader("fixtures/products_fixture.json").load()

        elif choice == "6":
            print("⚠️ FULL RESET...")
            DatabaseCleaner(db_file).clean()
            PycacheCleaner(apps_path).clean()
            MigrationsCleaner(apps_path).clean()
            # MigrationAndSuperuser().run()
            print("🚀 FULL RESET DONE!")

        elif choice == "7":
            MigrationAndSuperuser().run()
            GenerateFixtures().run()

        elif choice == "0":
            print("Bye 👋")
            break

        else:
            print("Invalid option!")
