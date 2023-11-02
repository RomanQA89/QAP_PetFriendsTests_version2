import logging

# Создаем логгер
logger = logging.getLogger('requests')
logger.setLevel(logging.INFO)

# Создаем обработчик для записи в файл
file_handler = logging.FileHandler('log.txt')
file_handler.setLevel(logging.INFO)

# Создаем форматтер для логов
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
logger.addHandler(file_handler)


def log_requests(func):
    def wrapper(*args, **kwargs):

        # Логируем запрос

        logger.info('Requests:')
        logger.info('URL: {}'.format(args[0]))
        logger.info('Method: {}'.format(func.__name__))
        logger.info('Arguments: {}'.format(args[1:]))
        logger.info('Keyword Arguments: {}'.format(kwargs))

        # Вызываем функцию и получаем результат
        result = func(*args, **kwargs)

        # Логируем ответ
        logger.info('Response:')
        logger.info('Status Code: {}'.format(result[0]))
        logger.info('Response Body: {}'.format(result[1]))

        # Возвращаем результат
        return result
    return wrapper
