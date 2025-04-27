from pathlib import Path

from .path import glob

DEFAULT_CONFIG = """\
${XDG_RUNTIME_DIR}/wayland-\\d+
${XDG_RUNTIME_DIR}/pipewire-\\d+
"""


def parse_config(config_path: Path):
    res = set()
    with open(config_path) as file:
        for line in file:
            res |= glob(line)
    return res


def load_config(config_path: Path, name: str):
    path = config_path / 'apps' / name
    if path.exists():
        return parse_config(path)
    path = config_path / 'default.cfg'
    if not path.exists():
        path.parent.mkdir(parents=True)
        with open(path, 'w') as file:
            file.write(DEFAULT_CONFIG)
    return parse_config(path)
