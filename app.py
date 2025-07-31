from parsers.chrome_parser import ChromeParser
from parsers.file_parser import FileParser
from questioner import questioner
from user_answers import AppMode

if __name__ == "__main__":
    user_answers = questioner.question_user()
    print(user_answers)

    if user_answers.app_mode == AppMode.FROM_URL:
        parser = ChromeParser(user_answers)
    else:
        parser = FileParser(user_answers)

    ...