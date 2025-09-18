# from pathlib import Path
# import shutil

# base = Path("./apps")
# db_file = Path("./database/db.sqlite3")

# # remove SQLite file if exists
# if db_file.exists():
#     if db_file.is_file():
#         print(f"Removing SQLite file: {db_file}")
#         db_file.unlink()
#     else:
#         print(f"{db_file} is not a file, skipping...")
# else:
#     print("No SQLite file found")

# # remove __pycache__ dirs
# if base.exists() and base.is_dir():
#     print("Apps dir exists")
#     removed = False
#     for path in base.rglob("*"):
#         if "__pycache__" in path.parts and path.is_dir():
#             print(f"Removing pycache dir: {path}")
#             shutil.rmtree(path)
#             removed = True
#     if not removed:
#         print("No __pycache__ directories found")
# else:
#     print("Apps dir does not exist")


from pathlib import Path
import shutil


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


# --- usage ---
if __name__ == "__main__":
    base = Path("./apps")
    db_file = Path("./database/db.sqlite3")

    DatabaseCleaner(db_file).clean()
    PycacheCleaner(base).clean()
    MigrationsCleaner(base).clean()  # <-- added here
