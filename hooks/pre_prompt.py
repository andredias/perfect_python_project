import os
import json
import sys
from pathlib import Path

config = Path("cookiecutter.json")
data = json.loads(config.read_text())
data["worker_class"] = "uvloop" if os.name == "posix" else "asyncio"
data["python_version"] = f"{sys.version_info.major}.{sys.version_info.minor}"
config.write_text(json.dumps(data, indent=4))
