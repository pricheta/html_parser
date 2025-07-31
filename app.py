from parsers.chrome_parser import ChromeParser
from parsers.file_parser import FileParser
from question_user import Questionary


if __name__ == "__main__":
    questionary = Questionary()
    user_answers = questionary.question_user()

    if user_answers.use_url:
        parser = ChromeParser(user_answers)
    else:
        parser = FileParser(user_answers)

    ...