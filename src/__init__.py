import logging
import os


if os.environ['LOG'] == 'DEB':
    level = logging.DEBUG
elif os.environ['LOG'] == 'INF':
    level = logging.INFO
elif os.environ['LOG'] == 'WAR':
    level = logging.WARN
elif os.environ['LOG'] == 'ERR':
    level = logging.ERROR
else:
    level = logging.INFO

logging.basicConfig(level=level,
                    format='%(levelname)s:%(asctime)s - %(message)s')

logging.info('Initializing n4j global server...')
