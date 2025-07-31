import questionary

from models import user_answers

def main() -> None:
    ask_user(
        url=questionary.text('Введите ссылку для парсера. Если не указана ссылка, будет использовано содержимое файла files/file.htm:')
    )



def ask_user(**kwargs) -> None:
    answers_dict = questionary.form(**kwargs).ask()
    for param, answer in answers_dict.items():
        user_answers.__setattr__(param, answer)


if __name__ == "__main__":
    main()
