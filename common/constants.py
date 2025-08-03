import pytz

FILES_DIR = './files/'
HTML_FILENAME = 'file.html'
RESULT_FILENAME = 'Результат от {}.xlsx'
RESULT_FILENAME_DATETIME_PATTERN = '%d_%m_%Y %H_%M MSK'

SSL_HEADER = 'https://'

MSK_TIMEZONE = pytz.timezone('Europe/Moscow')
DATETIME_PATTERN = '%d.%m.%Y %H:%M UTC'


LOG_FILENAME = 'logs.log'
LOG_FILE_MAX_SIZE_BYTES = 512 * 1024