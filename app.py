from parsers.chrome_parser import ChromeParser
from parsers.file_parser import FileParser
from questioner import questioner

if __name__ == "__main__":
    user_answers = questioner.question_user()

    if user_answers.use_url:
        parser = ChromeParser(user_answers)
    else:
        parser = FileParser(user_answers)

    ...