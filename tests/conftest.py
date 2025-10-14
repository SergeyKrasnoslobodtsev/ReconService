import sys
import os
from pathlib import Path


project_root = Path(__file__).parent.parent.parent.resolve()


if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

print(f"Добавлен в PYTHONPATH: {project_root}")

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')