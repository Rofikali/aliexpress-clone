import os
import sys
import subprocess
import shutil
import django
import time
from pathlib import Path
from django.core.management import call_command
from threading import Thread


# ------------------------------
# Spinner for long-running tasks
# ------------------------------
class Spinner:
    """A simple terminal spinner for long-running tasks."""

    def __init__(self, message="Processing..."):
        self.message = message
        self.running = False
        self.spinner_cycle = ["|", "/", "-", "\\"]
        self.fixture_file = "./full_fixture.json"  # <--- add this line here

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
            time.sleep(0.1)

    def stop(self):
        self.running = False
        print("\r", end="")


# ------------------------------
# Helpers
# ------------------------------
def run_cmd(cmd, show_spinner=True, message=None):
    """Run shell command with optional spinner."""
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


# ------------------------------
# Cleaners
# ------------------------------
class Cleaner:
    def __init__(self, path: Path):
        self.path = path

    def exists(self) -> bool:
        return self.path.exists()


class DatabaseCleaner(Cleaner):
    def clean(self, use_spinner=True):
        if not self.exists():
            print("No SQLite file found")
            return
        if self.path.is_file():
            if use_spinner:
                spinner = Spinner("Deleting database file")
                spinner.start()
                time.sleep(1)
                self.path.unlink()
                spinner.stop()
            else:
                self.path.unlink()
            print(f"✅ Database file removed: {self.path}")
        else:
            print(f"{self.path} exists but is not a file, skipping...")


class PycacheCleaner(Cleaner):
    def clean(self, use_spinner=True):
        if not self.exists() or not self.path.is_dir():
            print("Apps dir does not exist")
            return
        removed = False
        for path in self.path.rglob("*"):
            if "__pycache__" in path.parts and path.is_dir():
                if use_spinner:
                    spinner = Spinner(f"Removing __pycache__: {path}")
                    spinner.start()
                    time.sleep(0.2)
                    shutil.rmtree(path)
                    spinner.stop()
                else:
                    shutil.rmtree(path)
                print(f"✅ Removed: {path}")
                removed = True
        if not removed:
            print("No __pycache__ directories found")


class MigrationsCleaner(Cleaner):
    def clean(self, use_spinner=True):
        if not self.exists() or not self.path.is_dir():
            print("Apps dir does not exist")
            return
        removed = False
        for path in self.path.rglob("migrations"):
            if path.is_dir():
                for file in path.iterdir():
                    if file.suffix == ".py" and file.name != "__init__.py":
                        if use_spinner:
                            spinner = Spinner(f"Removing migration file: {file}")
                            spinner.start()
                            time.sleep(0.2)
                            file.unlink()
                            spinner.stop()
                        else:
                            file.unlink()
                        print(f"✅ Removed: {file}")
                        removed = True
        if not removed:
            print("No migration files found")


# ----------------------------------------------
# Migration + Superuser setup
# ------------------------------
class MigrationAndSuperuser:
    def run(self, use_spinner=True):
        if use_spinner:
            run_cmd(
                "python manage.py makemigrations home accounts products orders carts search",
                show_spinner=True,
                message="Making migrations",
            )
            run_cmd(
                "python manage.py migrate",
                show_spinner=True,
                message="Applying migrations",
            )
        else:
            run_cmd(
                "python manage.py makemigrations home accounts products orders carts search",
                show_spinner=False,
            )
            run_cmd("python manage.py migrate", show_spinner=False)

        print("Checking for existing superuser...")

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings.dev")
        django.setup()

        from apps.accounts.models import User

        if not User.objects.filter(is_superuser=True).exists():
            if use_spinner:
                spinner = Spinner("Creating superuser")
                spinner.start()
                time.sleep(1)
                User.objects.create_superuser(
                    username="admin", email="admin@gmail.com", password="admin"
                )
                spinner.stop()
            else:
                User.objects.create_superuser(
                    username="admin", email="admin@gmail.com", password="admin"
                )
            print("✅ Superuser created!")
        else:
            print("Superuser already exists.")


# ------------------------------
# Menu
# ------------------------------
def menu():
    print("\n=== Main Menu ===")
    print("1. Remove database file")
    print("2. Remove __pycache__ directories")
    print("3. Remove migration files")
    print("4. Run migrations & ensure superuser")
    print("5. All models: generate all models JSON & imports")
    print("6. Run ALL (with global spinner + elapsed time)")
    print("0. Exit")
    return input("Choose an option: ").strip()


# ------------------------------
# Main Loop
# ------------------------------
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings.dev")
    django.setup()

    base = Path("./apps")
    db_file = Path("./database/db.sqlite3")

    while True:
        choice = menu()

        if choice == "1":
            DatabaseCleaner(db_file).clean()
            # python manage.py flush
        elif choice == "2":
            PycacheCleaner(base).clean()
        elif choice == "3":
            MigrationsCleaner(base).clean()
        elif choice == "4":
            MigrationAndSuperuser().run()

        elif choice == "5":
            spinner = Spinner("Seeding homepage")
            spinner.start()
            os.system("python manage.py generate_fixtures")
            os.system("python manage.py generate_homepage_fixtures")
            spinner.stop()
            print("✅ Homepage seeded!")
        elif choice == "6":
            fixture_file = "./full_fixture.json"  # <--- add this line here
            confirm = (
                input(
                    "\n⚠️ This will remove DB, __pycache__, migrations, run migrations, "
                    "create superuser, import products, and seed homepage.\n"
                    "Are you sure? (y/n): "
                )
                .strip()
                .lower()
            )
            if confirm in ("y", "yes"):
                start_time = time.time()
                spinner = Spinner("Running ALL tasks")
                spinner.start()

                DatabaseCleaner(db_file).clean(use_spinner=False)
                PycacheCleaner(base).clean(use_spinner=False)
                MigrationsCleaner(base).clean(use_spinner=False)
                MigrationAndSuperuser().run(use_spinner=False)
                os.system("python manage.py generate_fixtures")
                os.system("python manage.py generate_homepage_fixtures")

                spinner.stop()
                elapsed = time.time() - start_time
                print("✅ ALL steps completed!")
                print(f"⏱ Total elapsed time: {elapsed:.2f} seconds")
            else:
                print("❌ Cancelled running ALL.")
        elif choice == "0":
            print("Bye 👋")
            break
        else:
            print("❌ Invalid option, please try again.")
