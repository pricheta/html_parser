import questionary

from common.constants import SSL_HEADER
from common.utils import clear_screen
from questioner.user_answers import UserAnswers, AppMode


class Questioner:
    def __init__(self):
        self.user_answers = UserAnswers()

    def question_user(self) -> UserAnswers:
        clear_screen()

        self._ask_user(
            app_mode=questionary.select(
                "Режим работы приложения",
                [AppMode.FROM_URL, AppMode.FROM_FILE, ],
                instruction=' ',
            ),
        )

        if self.user_answers.app_mode == AppMode.FROM_URL:
            self._ask_user(
                get_to_slave_page=questionary.confirm("Нужно ли будет переходить на вторичные страницы?"),
                url=questionary.text('Ссылка на основную страницу для парсинга:', validate=bool),
                master_page_parsed_classes=questionary.text("Введи классы элементов для парсинга на основной странице:", validate=bool),
            )
            if self.user_answers.get_to_slave_page:
                self._ask_user(
                    slave_page_parsed_classes=questionary.text("Введи классы элементов для парсинга на вторичных страницах:", validate=bool),
                    clicked_classes=questionary.text("Введи классы элементов, на которые нужно нажать для перехода на вторичные страницу:", validate=bool),
                )
            if SSL_HEADER not in self.user_answers.url:
                self.user_answers.url = SSL_HEADER + self.user_answers.url
        else:
            self._ask_user(
                master_page_parsed_classes=questionary.text("Введи классы элементов для парсинга на странице:", validate=bool),
            )

        return self.user_answers

    def _ask_user(self, **kwargs) -> None:
        answers_dict = questionary.form(**kwargs).ask()
        for param, answer in answers_dict.items():
            setattr(self.user_answers, param, answer)


questioner = Questioner()
