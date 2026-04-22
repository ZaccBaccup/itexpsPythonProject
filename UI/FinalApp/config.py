from pathlib import Path

# Directory where this config.py file lives
# __file__ = the path to config.py
# .resolve().parent = the folder containing that file
BASE_DIR = Path(__file__).resolve().parent

# data directory inside the project
OUTPUT_DIR = BASE_DIR / "data"
