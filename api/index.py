import sys
import os

# Insert backend directory into Python path so 'app.*' imports work seamlessly
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.abspath(os.path.join(current_dir, "..", "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Ensure serverless defaults for Vercel
if os.environ.get("VERCEL"):
    os.environ.setdefault("DATABASE_URL", "sqlite:////tmp/woodplan.db")
    os.environ.setdefault("STORAGE_DIR", "/tmp/storage")

from app.main import app
