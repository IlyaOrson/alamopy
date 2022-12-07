from pathlib import Path

base_path = Path.home()
# base_path = Path("/home/io")  # wsl
# base_path = Path("/content/")  # collab

exec_path = base_path / "alamo-linux64" / "alamo"

print(f"Expected ALAMO executable location: {exec_path}")
