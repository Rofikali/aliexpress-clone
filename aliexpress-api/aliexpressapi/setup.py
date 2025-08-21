
import os
import sys
import subprocess
import django

def run_cmd(cmd):
    """Run shell command and stream output"""
    print(f"\n🚀 Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Command failed: {cmd}")
        sys.exit(result.returncode)


def main():
    # Step 1: makemigrations for specific apps
    run_cmd("python manage.py makemigrations accounts products orders carts")

    # Step 2: migrate
    run_cmd("python manage.py migrate")

    # Step 3: auto-create superuser if not exists
    print("\n👤 Checking for existing superuser...")

    # ✅ set correct settings module ## Dev or Prod
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configs.settings.dev")
    django.setup()

    from apps.accounts.models import User  # adjust if your custom user model is elsewhere

    if not User.objects.filter(is_superuser=True).exists():
        print("⚡ Creating default superuser (admin1 / admin@gmail.com / admin1)")
        User.objects.create_superuser(
            username="admin1",
            email="admin@gmail.com",
            password="admin1"
        )
    else:
        print("✅ Superuser already exists. Skipping creation.")


if __name__ == "__main__":
    main()
