import sys

if len(sys.argv) != 3:
    print('Usage: prog INPUT_FILE OUTPUT_FILE')
    exit(1)

slides = [[[]]]  # slides[slide_number][command_number][line_number]
with open(sys.argv[1]) as file:
    CON, END = file.readline()[:2]

    for line in file.read().splitlines():
        last_slide = slides[-1]
        if line == '':
            if last_slide != [[]]:
                slides.append([[]])
            continue
        last_command = last_slide[-1]

        if not line.startswith(CON):
            pos = line.find(END) + 1
            assert pos, 'unknown format'
            last_command.append(line[:pos])
            next_command = line[pos:]
            if next_command and not next_command.isspace():
                last_slide.append([' ' * pos + next_command])
        else:
            last_command.append(line[1:])


with open(sys.argv[2], 'w') as file:
    nslides = len(slides)
    for i, slide in enumerate(slides):
        commands = []
        line_number = 0
        for command in slide:
            commands.append(f'{"\n" * line_number}{"\n".join(command)}')
            line_number += len(command) - 1

        ncommands = len(commands)
        for j, command in enumerate(reversed(commands)):
            file.seek(0)
            file.truncate()
            file.write(command)
            file.flush()
            input(f'slide={i + 1}/{nslides} command={j + 1}/{ncommands} ')
