import subprocess
import json
from pathlib import Path


class ExifTool:
    def __init__(self, executable: Path):
        self.executable = executable

    def get_metadata(self, path: Path):
        out = subprocess.check_output([self.executable, "-G", "-j", "-n", path])
        return json.loads(out)
