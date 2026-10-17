import sys
import os

# Add root directory to sys.path so 'backend' package is importable
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from backend.main import app

# Vercel looks for 'app' by default
__all__ = ["app"]
