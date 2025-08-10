import pytz

FILES_DIR = './files/'
HTML_FILENAME = 'file.html'
RESULT_FILENAME = 'Результат от {}.xlsx'

SSL_HEADER = 'https://'

MSK_TIMEZONE = pytz.timezone('Europe/Moscow')
DATETIME_PATTERN = '%d.%m.%Y %H:%M:%S'
RESULT_FILENAME_DATETIME_PATTERN = DATETIME_PATTERN.replace('.', '_').replace(':', '_')

LOG_FILENAME = 'logs.log'
LOG_FILE_MAX_SIZE_BYTES = 128 * 1024
