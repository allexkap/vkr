import argparse
import logging
import os
import shlex
from pathlib import Path
from shutil import rmtree

RUN_DIRS = ['wayland-1', 'pipewire-0', 'pulse']

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s %(filename)s:%(lineno)d %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, default='')
    parser.add_argument('-r', '--remove', action='store_true')
    parser.add_argument('-p', '--private', action='store_true')
    parser.add_argument('-c', '--current-dir', action='store_true')
    parser.add_argument('--path', type=Path, default='~/.local/state/vkr')
    parser.add_argument('--bwrap-args', type=str)
    parser.add_argument('inner', nargs=argparse.REMAINDER)

    args = parser.parse_args()
    if not args.inner:
        args.inner = ['bash']
    if args.name == '':
        args.name = Path(args.inner[0]).name
    args.path = args.path.expanduser() / args.name
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

    if args.remove:
        rmtree(args.path)
        exit(0)

    if not args.path.exists():
        args.path.mkdir(parents=True)

    flags = [
        '--unshare-all',
        '--die-with-parent',
    ]

    # fmt:off
    special_dirs = [
        '--ro-bind', '/', '/',
        '--proc', '/proc',
        '--dev', '/dev',
    ]
    # fmt:on

    home_dirs = []
    if args.private:
        home_dirs.extend(['--tmpfs', os.environ['HOME']])
    else:
        home_dirs.extend(['--bind', args.path.as_posix(), os.environ['HOME']])

    other_dirs = []
    if args.current_dir:
        home_dirs.extend(['--bind', os.getcwd(), os.getcwd()])

    xdg_runtime_dir = os.environ['XDG_RUNTIME_DIR']
    run_dirs = ['--tmpfs', '/run']
    for d in RUN_DIRS:
        d = f'{xdg_runtime_dir}/{d}'
        run_dirs.extend(['--bind', d, d])

    passthrough_args = []
    if args.bwrap_args is not None:
        passthrough_args.extend(shlex.split(args.bwrap_args))

    bwrap_args = [
        'bwrap',
        *flags,
        *special_dirs,
        *home_dirs,
        *run_dirs,
        *other_dirs,
        *passthrough_args,
        *args.inner,
    ]

    logging.debug(' '.join(bwrap_args))
    os.execvp(bwrap_args[0], bwrap_args)


if __name__ == '__main__':
    main()
