import os


def clear_screen() -> None:
    command = 'clear'
    if os.name == 'nt':
        command = 'cls'
    os.system(command)
