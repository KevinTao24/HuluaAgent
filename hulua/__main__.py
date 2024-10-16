import os
import sys

import uvicorn

sys.path.insert(0, os.path.dirname(__file__) + "/..")
from hulua.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "hulua.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
        factory=True,
    )


if __name__ == "__main__":
    main()
