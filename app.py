import os

import questionary

from models import user_answers


def main() -> None:
    clear_screen()

    ask_user(
        use_url=questionary.confirm("Использовать ссылку? Если нет, будет использовано содержимое файла files/file.htm"),
    )

    if user_answers.use_url:
        ask_user(url=questionary.text('Ссылка для перехода:'))


def ask_user(**kwargs) -> None:
    answers_dict = questionary.form(**kwargs).ask()
    for param, answer in answers_dict.items():
        user_answers.__setattr__(param, answer)

def clear_screen() -> None:
    command = 'clear'
    if os.name == 'nt':
        command = 'cls'
    os.system(command)


if __name__ == "__main__":
    main()
