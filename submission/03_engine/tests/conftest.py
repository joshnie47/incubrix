import os
import sys

# Ensure submission/03_engine is in sys.path for test imports
engine_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if engine_root not in sys.path:
    sys.path.insert(0, engine_root)
