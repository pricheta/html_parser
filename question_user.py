import os

import questionary

from constants import SSL_HEADER
from models import user_answers


def question_user() -> None:
    clear_screen()
    user_answers.clear()

    ask_user(
        use_url=questionary.confirm("Использовать ссылку? Если нет, будет использовано содержимое файла files/file.htm"),
    )

    if user_answers.use_url:
        ask_user(
            get_to_slave_page=questionary.confirm("Нужно ли будет переходить на вторичные страницы?"),
        )

    if user_answers.use_url:
        ask_user(url=questionary.text('Ссылка на основную страницу для парсинга:', validate=bool))
        if SSL_HEADER not in user_answers.url:
            user_answers.url = SSL_HEADER + user_answers.url

    ask_user(
        master_page_parsed_classes=questionary.text("Введи классы элементов для парсинга на основной странице:", validate=bool),
    )

    if user_answers.get_to_slave_page:
        ask_user(
            clicked_classes=questionary.text("Введи классы элементов, на которые нужно нажать для перехода на вторичные страницу:", validate=bool),
            slave_page_parsed_classes=questionary.text("Введи классы элементов для парсинга на вторичных страницах:", validate=bool),
        )


def ask_user(**kwargs) -> None:
    answers_dict = questionary.form(**kwargs).ask()
    for param, answer in answers_dict.items():
        setattr(user_answers, param, answer)


def clear_screen() -> None:
    command = 'clear'
    if os.name == 'nt':
        command = 'cls'
    os.system(command)
