# import subprocess
# import time
# import socket


# def port_open(port):
#     """Check if a port is open."""
#     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s.settimeout(1)
#     return s.connect_ex(("127.0.0.1", port)) == 0


# class ServerRunner:
#     def __init__(self, name, cwd, command, port):
#         self.name = name
#         self.cwd = cwd
#         self.command = command
#         self.port = port

#     def start(self):
#         print(f"\n🚀 Starting {self.name}...")

#         for attempt in range(1, 3):
#             print(f"   Attempt {attempt}/3...")

#             try:
#                 # Open NEW terminal window
#                 subprocess.Popen(
#                     f'start cmd /k "{self.command}"', cwd=self.cwd, shell=True
#                 )

#                 # Wait for server to boot
#                 for i in range(10):
#                     if port_open(self.port):
#                         print(f"   ✔ {self.name} is running on port {self.port}!")
#                         return True
#                     time.sleep(1)

#                 print(f"   ❌ {self.name} failed to start on attempt {attempt}")

#             except Exception as e:
#                 print(f"   ❌ Error: {e}")

#         print(f"❌ FAILED to start {self.name} after 3 attempts.\n")
#         return False


# class ProjectLauncher:
#     def __init__(self):
#         self.django = ServerRunner(
#             name="Django Server",
#             cwd=r"C:\Py-Apis\aliexpress-clone\aliexpress-api\aliexpressapi",
#             command="uv run manage.py runserver",
#             port=8000,
#         )

#         self.nuxt = ServerRunner(
#             name="Nuxt 4 Dev Server",
#             cwd=r"C:\Py-Apis\aliexpress-clone\aliexpress-nuxt4",
#             command="pnpm run dev",
#             port=3000,
#         )

#     def launch_all(self):
#         print("\n==============================")
#         print(" Starting All Dev Servers")
#         print("==============================")

#         self.django.start()
#         self.nuxt.start()

#         print("\n🔥 All servers launched in separate terminals!\n")


# if __name__ == "__main__":
#     launcher = ProjectLauncher()
#     launcher.launch_all()


#!/usr/bin/env python3
"""
UV & YAML Dev Launcher

Run:
    uv run ./run_servers.py start
"""

from pathlib import Path
import subprocess
import os
import sys
import logging
import platform
import time
import socket
import secrets
import string
import shutil

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml")
    sys.exit(1)

try:
    import psutil
except ImportError:
    psutil = None

# -------------------------
# Globals
# -------------------------
ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"
LOGS.mkdir(exist_ok=True)
LOG_FILE = LOGS / "dev.log"

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(console_handler)

SYSTEM = platform.system()


# -------------------------
# Utilities
# -------------------------
def port_open(port, host="127.0.0.1"):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.8)
    try:
        return s.connect_ex((host, port)) == 0
    finally:
        s.close()


def generate_secret_key(length=50):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    filtered = alphabet.replace('"', "").replace("'", "").replace("\\", "")
    return "".join(secrets.choice(filtered) for _ in range(length))


def find_venv(base: Path):
    names = [".venv", "venv", "env", ".env"]
    p = base.resolve()
    for folder in [p] + list(p.parents):
        for n in names:
            c = folder / n
            if c.exists():
                return c
    return None


def venv_python(venv_path: Path):
    if not venv_path:
        return None
    if SYSTEM == "Windows":
        exe = venv_path / "Scripts" / "python.exe"
    else:
        exe = venv_path / "bin" / "python"
    return exe if exe.exists() else None


def prep_env(venv_path: Path):
    env = os.environ.copy()
    if not venv_path:
        return env
    if SYSTEM == "Windows":
        bin_dir = venv_path / "Scripts"
    else:
        bin_dir = venv_path / "bin"
    env["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")
    env["VIRTUAL_ENV"] = str(venv_path)
    return env


def run_cmd(cmd, cwd=None, env=None, shell=True, check=False, capture_output=False):
    logging.info(f"CMD: {cmd} (cwd={cwd})")
    try:
        res = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            env=env,
            shell=shell,
            check=check,
            capture_output=capture_output,
            text=True,
        )
        if capture_output:
            return res.stdout.strip()
        return res
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {cmd} {e}")
        raise


# -------------------------
# Service Model
# -------------------------
class Service:
    def __init__(self, name, cfg, root: Path, defaults: dict):
        self.name = name
        self.root = root
        self.cfg = cfg or {}
        self.type = (self.cfg.get("type") or "").lower()
        self.path = (root / (self.cfg.get("path") or "")).resolve()
        self.port = int(self.cfg.get("port") or 0)
        self.run_cmd = self.cfg.get("run") or ""
        self.venv_cfg = self.cfg.get("venv")
        self.venv = (
            (root / self.venv_cfg).resolve()
            if self.venv_cfg
            else find_venv(self.path) or find_venv(root)
        )
        self.process = None

    def prepare(self):
        logging.info(f"Preparing service: {self.name} (type={self.type})")
        if not self.path.exists():
            logging.warning(f"Path missing for {self.name}: {self.path} — creating")
            self.path.mkdir(parents=True, exist_ok=True)

        # Django .env
        if self.type == "django":
            env_path = self.path / ".env"
            if not env_path.exists():
                logging.info(f"Generating .env for {self.name} at {env_path}")
                env_path.write_text(f"SECRET_KEY={generate_secret_key()} DEBUG=True\n")

        # Install dependencies
        installs = self.cfg.get("install") or []
        for item in installs:
            if isinstance(item, dict):
                tool, arg = next(iter(item.items()))
            elif isinstance(item, str) and ":" in item:
                tool, arg = [p.strip() for p in item.split(":", 1)]
            else:
                logging.warning(f"Unknown install instruction: {item}")
                continue

            if tool == "pip":
                req = (self.path / arg).resolve()
                py = (
                    venv_python(self.venv)
                    or shutil.which("python")
                    or shutil.which("python3")
                )
                if req.exists() and py:
                    run_cmd(f'"{py}" -m pip install -r "{req}"', cwd=self.path)
                else:
                    logging.info(f"No requirements at {req}; skipping pip install")
            elif tool == "uv":
                pyproject = (self.path / arg).resolve()
                if pyproject.exists():
                    run_cmd(f'uv pip install -r "{pyproject}"', cwd=self.path)
                else:
                    logging.warning(f"pyproject not found at {pyproject}")
            elif tool in ("pnpm", "npm"):
                pkg = self.path / "package.json"
                if pkg.exists():
                    if shutil.which("pnpm"):
                        run_cmd("pnpm install", cwd=self.path)
                    elif shutil.which("corepack"):
                        run_cmd("corepack enable", shell=True)
                        run_cmd("corepack prepare pnpm@latest --activate", shell=True)
                        run_cmd("pnpm install", cwd=self.path)
                    else:
                        logging.warning("pnpm not found: install Node/corepack/pnpm")
                else:
                    logging.info("No package.json; skipping node install")
            else:
                logging.warning(f"Unsupported install tool: {tool}")

    def start(self, wait_for_port=True, attempts=3, timeout=12):
        logging.info(f"Starting {self.name}")
        self.prepare()
        env = prep_env(self.venv)
        cmd = self.run_cmd

        # uv run commands should not be rewritten
        vpy = venv_python(self.venv)
        if vpy and cmd.strip().startswith("python "):
            cmd = f'"{vpy}" ' + cmd.strip()[7:]

        for attempt in range(1, attempts + 1):
            print(f"   Attempt {attempt}/{attempts}...")
            try:
                if SYSTEM == "Windows":
                    start_cmd = f'start cmd /k "cd {self.path} && {cmd}"'
                    proc = subprocess.Popen(
                        start_cmd, cwd=str(self.path), shell=True, env=env
                    )
                elif SYSTEM == "Darwin":
                    apple = f'tell application "Terminal" to do script "cd {self.path} && {cmd}"'
                    proc = subprocess.Popen(["osascript", "-e", apple], env=env)
                else:
                    terminals = ["gnome-terminal", "konsole", "xterm", "xfce4-terminal"]
                    opened = False
                    for term in terminals:
                        if shutil.which(term):
                            full = f'{term} -- bash -c "cd {self.path} && {cmd}; exec bash"'
                            proc = subprocess.Popen(full, shell=True, env=env)
                            opened = True
                            break
                    if not opened:
                        bg = (
                            f'nohup bash -c "cd {self.path} && {cmd}" >/dev/null 2>&1 &'
                        )
                        proc = subprocess.Popen(bg, shell=True, env=env)

                self.process = proc

                if wait_for_port and self.port:
                    waited = 0
                    while waited < timeout:
                        if port_open(self.port):
                            print(f"   ✔ {self.name} is running on port {self.port}!")
                            logging.info(f"{self.name} listening on {self.port}")
                            return True
                        time.sleep(1)
                        waited += 1
                    print(f"   ❌ {self.name} didn't open port in time")
                else:
                    logging.info(f"Launched {self.name} (not waiting for port)")
                    return True
            except Exception as e:
                logging.error(f"Error starting {self.name}: {e}")
                print(f"   ❌ Error: {e}")
            time.sleep(1)
        logging.error(f"Failed to start {self.name}")
        return False

    def stop(self):
        logging.info(f"Stopping {self.name}")
        print(f"Stopping {self.name} (port {self.port})...")
        if self.process:
            try:
                self.process.terminate()
            except Exception:
                pass

        if self.port:
            killed = False
            if psutil:
                for proc in psutil.process_iter(["pid", "name"]):
                    try:
                        for con in proc.connections(kind="inet"):
                            if con.laddr.port == self.port:
                                proc.kill()
                                killed = True
                    except Exception:
                        continue
            else:
                if SYSTEM == "Windows":
                    try:
                        out = run_cmd(
                            f"netstat -ano | findstr :{self.port}", capture_output=True
                        )
                        if out:
                            for line in out.splitlines():
                                pid = line.split()[-1]
                                run_cmd(f"taskkill /PID {pid} /F")
                                killed = True
                    except Exception:
                        pass
                else:
                    if shutil.which("fuser"):
                        try:
                            run_cmd(f"fuser -k {self.port}/tcp", shell=True)
                            killed = True
                        except Exception:
                            pass
            if killed:
                print(f"✔ Stopped processes on port {self.port}")
            else:
                print(f"⚠ No process found on port {self.port}")


# -------------------------
# DevLauncher
# -------------------------
class DevLauncher:
    def __init__(self, yaml_path: Path = None):
        self.root = ROOT
        self.yaml_path = yaml_path or (self.root / "dev.yaml")
        if not self.yaml_path.exists():
            logging.error(f"dev.yaml not found at {self.yaml_path}")
            raise FileNotFoundError("dev.yaml missing")
        self.cfg = yaml.safe_load(self.yaml_path.read_text())
        self.defaults = self.cfg.get("defaults", {})
        self.services = []
        for name, s in (self.cfg.get("services") or {}).items():
            self.services.append(Service(name, s, self.root, self.defaults))

    def start_all(self):
        print("=== Starting All Services ===")
        for s in self.services:
            s.start()
        print("=== All start attempts complete ===")

    def stop_all(self):
        print("=== Stopping All Services ===")
        for s in self.services:
            s.stop()
        print("=== All stop attempts complete ===")

    def status(self):
        print("=== Services Status ===")
        for s in self.services:
            alive = port_open(s.port) if s.port else False
            print(f"- {s.name}: port={s.port} alive={alive}")


# -------------------------
# CLI
# -------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: uv run ./run_servers.py <start|stop|restart|status>")
        sys.exit(1)
    cmd = sys.argv[1]
    launcher = DevLauncher()
    if cmd == "start":
        launcher.start_all()
    elif cmd == "stop":
        launcher.stop_all()
    elif cmd == "restart":
        launcher.stop_all()
        time.sleep(1)
        launcher.start_all()
    elif cmd == "status":
        launcher.status()
    else:
        print(
            "Unknown command. Usage: uv run ./run_servers.py <start|stop|restart|status>"
        )


if __name__ == "__main__":
    main()
