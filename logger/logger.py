import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs.log', encoding='utf-8'),
    ]
)

logger = logging.getLogger()
