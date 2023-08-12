import logging

main_logger = logging.getLogger(__name__)
main_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(filename='attachment/myapp.log', mode='w')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
main_logger.addHandler(file_handler)
