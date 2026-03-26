import logging


def setup_logging(level: int = logging.DEBUG) -> None:
    logging.basicConfig(
        level=level,
        format="%(levelname)s:%(name)s:%(message)s",
    )

    # suppress noisy debug logs from Pillow
    logging.getLogger("PIL").setLevel(logging.WARNING)
