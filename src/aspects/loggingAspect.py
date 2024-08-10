import logging


def setup_logger():
    logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s - %(message)s"
        )
