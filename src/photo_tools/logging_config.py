import logging
import os


def setup_logging() -> None:
    debug = os.getenv("PHOTO_TOOLS_DEBUG") == "1"
    level = logging.DEBUG if debug else logging.CRITICAL

    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(name)s: %(message)s",
        force=True,  # ensures config is applied even if already set
    )

    logging.getLogger("PIL").setLevel(logging.WARNING)
