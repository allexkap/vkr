import argparse
import logging
import os
import sys
from pathlib import Path

import mount

RUN_DIRS = ['wayland-1', 'pipewire-0', 'pulse']


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', type=Path, default='/var/tmp/vkr')
    parser.add_argument('-n', '--name', type=str, default='')
    parser.add_argument('inner', nargs=argparse.REMAINDER)

    args = parser.parse_args()
    if not args.inner:
        args.inner = ['bash']
    if args.name == '':
        args.name = Path(args.inner[0]).name
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

    flags = [
        '--unshare-all',
        '--die-with-parent',
    ]

    # fmt:off
    special_fs = [
        '--ro-bind', '/', '/',
        '--proc', '/proc',
        '--dev', '/dev',
    ]
    home_fs = [
        '--bind', args.path.as_posix(), '/home',
    ]
    # fmt:on

    xdg_runtime_dir = os.environ['XDG_RUNTIME_DIR']
    run_dirs = ['--tmpfs', '/run']
    for d in RUN_DIRS:
        d = f'{xdg_runtime_dir}/{d}'
        run_dirs.extend(['--bind', d, d])

    bwrap_args = [
        'bwrap',
        *flags,
        *special_fs,
        *home_fs,
        *run_dirs,
        *args.inner,
    ]

    print(' '.join(bwrap_args))
    os.execvp(bwrap_args[0], bwrap_args)


if __name__ == '__main__':
    main()
