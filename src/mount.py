import ctypes
import os
from pathlib import Path

MS_RDONLY = 1 << 1
MS_NOSUID = 1 << 2
MS_NODEV = 1 << 3
MS_NOEXEC = 1 << 4
MS_SYNCHRONOUS = 1 << 5
MS_REMOUNT = 1 << 6
MS_MANDLOCK = 1 << 7
MS_DIRSYNC = 1 << 8
MS_NOSYMFOLLOW = 1 << 9
MS_NOATIME = 1 << 10
MS_NODIRATIME = 1 << 11
MS_BIND = 1 << 12
MS_MOVE = 1 << 13
MS_REC = 1 << 14
MS_SILENT = 1 << 15
MS_POSIXACL = 1 << 16
MS_UNBINDABLE = 1 << 17
MS_PRIVATE = 1 << 18
MS_SLAVE = 1 << 19
MS_SHARED = 1 << 20
MS_RELATIME = 1 << 21
MS_KERNMOUNT = 1 << 22
MS_I_VERSION = 1 << 23
MS_STRICTATIME = 1 << 24
MS_LAZYTIME = 1 << 25


_libc = ctypes.CDLL(None, use_errno=True)


def mount(
    source: Path | None,
    target: Path,
    fs_type: str = '',
    flags: int = 0,
    data: str = '',
) -> None:
    if source is None:
        source = Path()
    if not target.exists():
        target.mkdir(parents=True)

    ret = _libc.mount(
        source.as_posix().encode(),
        target.as_posix().encode(),
        fs_type.encode(),
        flags,
        data.encode(),
    )
    if ret < 0:
        errno = ctypes.get_errno()
        raise OSError(errno, f'Mount failed: {os.strerror(errno)}')
