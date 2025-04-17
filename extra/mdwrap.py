import argparse
import re
import textwrap

import mistune
from mistune.renderers.markdown import MarkdownRenderer


def fill(text, width):
    return textwrap.fill(
        text,
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    )


class WrapRenderer(MarkdownRenderer):
    def __init__(self, width=80) -> None:
        super().__init__()
        self.wrap_width = width

    def softbreak(self, token, state) -> str:
        return ' '

    def paragraph(self, token, state) -> str:
        text = super().paragraph(token, state)
        lines = text.rstrip().splitlines()
        text = '  \n'.join(fill(line, self.wrap_width) for line in lines)
        return f'{text}\n\n'

    def heading(self, token, state) -> str:
        text = super().heading(token, state)
        if token['attrs']['level'] == 1:
            text = '\n' + text
        return text

    def list(self, token, state) -> str:
        text = super().list(token, state)
        text = re.sub('^(\\d+)(?=\\.)', '1', text, flags=re.MULTILINE)
        return text

    def block_text(self, token, state) -> str:
        text = super().block_text(token, state)
        text = fill(text, self.wrap_width - 3)
        return f'{text}'


def process(text):
    md = mistune.Markdown(renderer=WrapRenderer())
    text = str(md(text)).lstrip()
    # text = re.sub('^(#[^\n]+)\n+(?=\n\\w)', '\\1', text, flags=re.MULTILINE)
    # text = re.sub('^\n(?=1. )', '', text, flags=re.MULTILINE)
    return text


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--in-place', action='store_true', help='edit file in place'
    )
    parser.add_argument('file', type=str)
    parser.add_argument('output_file', type=str, nargs='?')
    args = parser.parse_args()
    if args.in_place:
        args.output_file = args.file
    return args


def main():
    args = parse_args()

    content = open(args.file, 'r').read()
    content = process(content)
    if args.output_file:
        with open(args.output_file, 'w') as file:
            file.write(content)
    else:
        print(content, end='')


if __name__ == '__main__':
    main()
