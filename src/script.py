import argparse
import logging
import os
import sys
from pathlib import Path

import mount

# todo
OVERLAY_DIRS = ['etc', 'root', 'srv', 'usr', 'var']
LINKS = [
    ('/bin', '/usr/bin'),
    ('/sbin', '/usr/bin'),
    # ('/usr/sbin/', '/usr/bin'),
    ('/lib', '/usr/lib'),
    ('/lib64', '/usr/lib'),
    # ('/var/run', '/run'),
]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=Path, default='/tmp/vkr')
    parser.add_argument('-n', '--name', type=str, default='')
    parser.add_argument('inner', nargs=argparse.REMAINDER)

    args = parser.parse_args()
    if not args.inner:
        args.inner = ['bash']
    if args.name == '':
        args.name = args.inner[0]
    args.path /= args.name
    return args


def write(path, *data):
    with open(path, 'w') as file:
        for line in data:
            file.write(line)


def cat(path):
    with open(path, 'r') as file:
        print(f'{repr(path)}:\n{repr(file.read())}')


def print_res_ug_id():
    for d, f in (('uid', os.getresuid), ('gid', os.getresgid)):
        print(d, *map('='.join, zip(('real', 'effective', 'saved'), map(str, f()))))


def main():
    args = parse_args()

    if not args.path.exists():
        args.path.mkdir(parents=True)

    uid, gid = os.getuid(), os.getgid()

    os.unshare(os.CLONE_NEWNS | os.CLONE_NEWUSER | os.CLONE_NEWPID)

    pid = os.fork()
    if pid:
        _, status = os.waitpid(pid, 0)
        assert os.WIFEXITED(status)
        exit(os.WEXITSTATUS(status))

    write('/proc/self/setgroups', 'deny')
    write('/proc/self/uid_map', f'0 {uid} 1')
    write('/proc/self/gid_map', f'0 {gid} 1')

    os.chdir(args.path)

    mount.mount(None, args.path / 'proc', 'proc')
    for dir in OVERLAY_DIRS:
        mount.mount(
            Path('/') / dir, args.path / dir, flags=mount.MS_BIND | mount.MS_SHARED
        )

    os.unshare(os.CLONE_NEWUSER)
    write('/proc/self/uid_map', f'{uid} 0 1')
    write('/proc/self/gid_map', f'{gid} 0 1')

    os.execvp(args.inner[0], args.inner)


if __name__ == '__main__':
    main()
