import os
import subprocess
import time
import socket
from pathlib import Path


# ===============================================
# PATH CONFIGURATION
# ===============================================

PROJECT_ROOT = Path(__file__).resolve().parent
DJANGO_DIR = PROJECT_ROOT / "aliexpress-api" / "aliexpressapi"
MANAGE = DJANGO_DIR / "manage.py"
ENV_FILE = PROJECT_ROOT / ".env"


# ===============================================
# STYLING HELPERS
# ===============================================


def line():
    print("============================================")


def run(cmd, cwd=None, exit_on_fail=False):
    """Run terminal commands with safety."""
    print(f"\n⚡ Running: {cmd}")
    try:
        subprocess.run(cmd, cwd=cwd, shell=True, check=True)
        print("✔ Success")
    except subprocess.CalledProcessError:
        print(f"⚠ Command failed but continuing: {cmd}")
        if exit_on_fail:
            exit()


# ===============================================
# STEP 1 — AUTO-GENERATE .env IF MISSING
# ===============================================


def create_env_file():
    print("\n🧪 Checking for .env file...")

    if ENV_FILE.exists():
        print("✔ .env already exists → skipping")
        return

    print("❌ .env missing → creating now...")

    ENV_FILE.write_text(
        "DEBUG=True\n"
        "SECRET_KEY=dev-secret-key\n"
        "DATABASE_NAME=db.sqlite3\n"
        "ALLOWED_HOSTS=*\n"
    )

    print("✔ .env created successfully!")


# ===============================================
# STEP 2 — CREATE SUPERUSER ONLY IF NOT EXISTS
# ===============================================


def create_superuser_if_not_exists():
    print("\n🧪 Checking for existing superuser...")

    check_cmd = (
        f'uv run "{MANAGE}" shell -c "'
        f"from django.contrib.auth import get_user_model; "
        f"User=get_user_model(); "
        f"import sys; "
        f"sys.exit(0) if User.objects.filter(username='admin').exists() else sys.exit(1)\""
    )

    exists = subprocess.run(check_cmd, cwd=DJANGO_DIR, shell=True).returncode == 0

    if exists:
        print("✔ Superuser exists → skipping")
        return

    print("❌ No admin found → creating superuser...")

    create_cmd = (
        f'uv run "{MANAGE}" shell -c "'
        f"from django.contrib.auth import get_user_model; "
        f"User=get_user_model(); "
        f"User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')\""
    )

    run(create_cmd, cwd=DJANGO_DIR)

    print("✔ Superuser created!")


# ===============================================
# STEP 3 — PORT CHECKER
# ===============================================


def port_open(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    return s.connect_ex(("127.0.0.1", port)) == 0


# ===============================================
# STEP 4 — SERVER RUNNER CLASS
# ===============================================


class ServerRunner:
    def __init__(self, name, cwd, command, port):
        self.name = name
        self.cwd = cwd
        self.command = command
        self.port = port

    def start(self):
        print(f"\n🚀 Launching {self.name}...")
        for attempt in range(1, 3):
            print(f"   🔄 Attempt {attempt}/2")

            subprocess.Popen(f'start cmd /k "{self.command}"', cwd=self.cwd, shell=True)

            for _ in range(12):
                if port_open(self.port):
                    print(f"   ✔ {self.name} running on port {self.port}")
                    return True
                time.sleep(1)

            print(f"   ❌ {self.name} failed this attempt")

        print(f"❌ FINAL FAIL → {self.name} did not start")
        return False


# ===============================================
# STEP 5 — MAIN SETUP WORKFLOW
# ===============================================


def main():
    line()
    print("🚀 Starting FULL Django + UV Setup (A→Z)")
    line()

    # Step 1 — env
    create_env_file()

    # Step 2 — ensure venv exists
    if not (PROJECT_ROOT / ".venv").exists():
        run("uv venv")
    else:
        print("✔ venv exists → skipping")

    # Step 3 — install dependencies
    run(
        "uv add django djangorestframework djangorestframework-simplejwt",
        cwd=PROJECT_ROOT,
    )

    # Step 4 — migrations
    run(f'uv run "{MANAGE}" makemigrations', cwd=DJANGO_DIR)
    run(f'uv run "{MANAGE}" migrate', cwd=DJANGO_DIR)

    # Step 5 — admin
    create_superuser_if_not_exists()

    # Step 6 — fake data load
    print("\n🧪 Loading fake data (if exists)...")
    run(f'uv run "{MANAGE}" loaddata fake_data.json', cwd=DJANGO_DIR)

    print("\n🎉 SETUP FINISHED SUCCESSFULLY!")

    # Launch both servers
    print("\n==============================")
    print("🔥 Launching Both Servers")
    print("==============================")

    django_server = ServerRunner(
        name="Django Server",
        cwd=DJANGO_DIR,
        command="uv run manage.py runserver",
        port=8000,
    )

    nuxt_server = ServerRunner(
        name="Nuxt 4 Dev Server",
        cwd=str(PROJECT_ROOT / "aliexpress-nuxt4"),
        command="pnpm run dev",
        port=3000,
    )

    django_server.start()
    nuxt_server.start()

    print("\n🔥 All done! Both servers launched.")


# ===============================================
# RUN SCRIPT
# ===============================================
if __name__ == "__main__":
    main()
