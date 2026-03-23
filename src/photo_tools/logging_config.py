import logging

def setup_logging(level=logging.DEBUG) -> None:
    logging.basicConfig(
        level=level,
        format="%(levelname)s:%(name)s:%(message)s",
    )