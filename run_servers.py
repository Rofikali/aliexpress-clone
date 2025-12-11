import subprocess
import time
import socket


def port_open(port):
    """Check if a port is open."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    return s.connect_ex(("127.0.0.1", port)) == 0


class ServerRunner:
    def __init__(self, name, cwd, command, port):
        self.name = name
        self.cwd = cwd
        self.command = command
        self.port = port

    def start(self):
        print(f"\n🚀 Starting {self.name}...")

        for attempt in range(1, 3):
            print(f"   Attempt {attempt}/3...")

            try:
                # Open NEW terminal window
                subprocess.Popen(
                    f'start cmd /k "{self.command}"', cwd=self.cwd, shell=True
                )

                # Wait for server to boot
                for i in range(10):
                    if port_open(self.port):
                        print(f"   ✔ {self.name} is running on port {self.port}!")
                        return True
                    time.sleep(1)

                print(f"   ❌ {self.name} failed to start on attempt {attempt}")

            except Exception as e:
                print(f"   ❌ Error: {e}")

        print(f"❌ FAILED to start {self.name} after 3 attempts.\n")
        return False


class ProjectLauncher:
    def __init__(self):
        self.django = ServerRunner(
            name="Django Server",
            cwd=r"C:\Py-Apis\aliexpress-clone\aliexpress-api\aliexpressapi",
            command="uv run manage.py runserver",
            port=8000,
        )

        self.nuxt = ServerRunner(
            name="Nuxt 4 Dev Server",
            cwd=r"C:\Py-Apis\aliexpress-clone\aliexpress-nuxt4",
            command="pnpm run dev",
            port=3000,
        )

    def launch_all(self):
        print("\n==============================")
        print(" Starting All Dev Servers")
        print("==============================")

        self.django.start()
        self.nuxt.start()

        print("\n🔥 All servers launched in separate terminals!\n")


if __name__ == "__main__":
    launcher = ProjectLauncher()
    launcher.launch_all()
