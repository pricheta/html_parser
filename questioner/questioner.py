import questionary

from common.utils import clear_screen
from logger.logger import logger, log_calling
from questioner.user_answers import UserAnswers, AppMode, MasterSlaveMode


class Questioner:
    def __init__(self):
        self.user_answers = UserAnswers()
        self.logger = logger

    @log_calling
    def question_user(self) -> UserAnswers:
        clear_screen()

        self._ask_user(app_mode=questionary.select("Режим работы приложения", [mode for mode in AppMode], instruction=' '))

        if self.user_answers.app_mode == AppMode.FROM_URL:
            self._ask_about_url_mode()
        else:
            self._ask_about_file_mode()

        self._log_answers()
        return self.user_answers

    def _ask_user(self, **kwargs) -> None:
        answers_dict = questionary.form(**kwargs).ask()
        for param, answer in answers_dict.items():
            setattr(self.user_answers, param, answer)

    def _log_answers(self) -> None:
        self.logger.info(f'User answered - {self.user_answers.model_dump(exclude_none=True)}')

    def _ask_about_url_mode(self):
        self._ask_user(master_slave_mode=questionary.select("Режим переходов на второстепенные страницы", [mode for mode in MasterSlaveMode], instruction=' '))
        self._ask_user(scroll_required=questionary.confirm("Нужно ли будет скроллить вниз основную страницу?"))
        self._ask_user(url=questionary.text('Ссылка на основную страницу для парсинга:', validate=bool))
        self._ask_user(master_page_parsed_selector=questionary.text("Введи классы элементов для парсинга на основной странице:", validate=bool))

        if self.user_answers.master_slave_mode == MasterSlaveMode.CLICK_INNER_TAG:
            self._ask_user(clicked_selector=questionary.text("Введи классы элементов, на которые нужно нажать для перехода на вторичные страницы:", validate=bool))

        if self.user_answers.master_slave_mode in (MasterSlaveMode.CLICK_MASTER_TAG, MasterSlaveMode.CLICK_INNER_TAG):
            self._ask_user(slave_page_parsed_selector=questionary.text("Введи классы элементов для парсинга на вторичных страницах:", validate=bool))

        self._ask_user(delay=questionary.text("Введи задержку между действиями:", validate=bool))

    def _ask_about_file_mode(self):
        self._ask_user(master_page_parsed_selector=questionary.text("Введи классы элементов для парсинга на странице:", validate=bool))

questioner = Questioner()
