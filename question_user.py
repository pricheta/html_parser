import questionary

from common import clear_screen
from constants import SSL_HEADER
from user_answers import UserAnswers

class Questionary:
    def __init__(self):
        self.user_answers = UserAnswers()

    def question_user(self) -> UserAnswers:
        clear_screen()

        self._ask_user(
            use_url=questionary.confirm("Использовать ссылку? Если нет, будет использовано содержимое файла files/file.htm"),
        )

        if self.user_answers.use_url:
            self._ask_user(
                get_to_slave_page=questionary.confirm("Нужно ли будет переходить на вторичные страницы?"),
            )

        if self.user_answers.use_url:
            self._ask_user(url=questionary.text('Ссылка на основную страницу для парсинга:', validate=bool))
            if SSL_HEADER not in self.user_answers.url:
                self.user_answers.url = SSL_HEADER + self.user_answers.url

        self._ask_user(
            master_page_parsed_classes=questionary.text("Введи классы элементов для парсинга на основной странице:", validate=bool),
        )

        if self.user_answers.get_to_slave_page:
            self._ask_user(
                clicked_classes=questionary.text("Введи классы элементов, на которые нужно нажать для перехода на вторичные страницу:", validate=bool),
                slave_page_parsed_classes=questionary.text("Введи классы элементов для парсинга на вторичных страницах:", validate=bool),
            )

        return self.user_answers


    def _ask_user(self, **kwargs) -> None:
        answers_dict = questionary.form(**kwargs).ask()
        for param, answer in answers_dict.items():
            setattr(self.user_answers, param, answer)
