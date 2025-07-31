from parsers.chrome_parser import ChromeParser
from parsers.file_parser import FileParser
from user_answers import user_answers
from question_user import question_user


if __name__ == "__main__":
    question_user()

    if user_answers.use_url:
        parser = ChromeParser(user_answers)
    else:
        parser = FileParser(user_answers)

    ...