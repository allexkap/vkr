import logging
import os
import re
from pathlib import Path


def sub_env(var):
    if var == '~':
        return str(Path.home())
    return os.environ[var[1]]


def expandvars(text):
    return re.sub('\\${(\\w+)}', sub_env, text)


def _glob(pattern: str, path: Path, dbg_offset='') -> set[Path]:
    if not pattern:
        return {path}

    curr, _, sub = pattern.partition('/')
    assert curr

    matched = set()
    logging.debug('%s %s%s', '?', dbg_offset, curr)
    for entry in path.iterdir():
        if re.fullmatch(curr, entry.name):
            logging.debug('%s %s%s', '+', dbg_offset, entry)
            try:
                matched |= _glob(sub, entry, dbg_offset + ' ')
            except PermissionError:
                logging.debug('%s %s%s', '~', dbg_offset, entry)
        else:
            logging.debug('%s %s%s', '-', dbg_offset, entry)
    return matched


def glob(pattern: str) -> set[Path]:
    pattern = pattern.strip()
    pattern = expandvars(pattern)
    if not pattern.startswith('/'):
        raise ValueError('incorrect pattern')
    pattern = re.sub('(^|(?<=/))/', '', pattern)
    logging.info(f'pattern={pattern}')
    return _glob(pattern, Path('/'))
