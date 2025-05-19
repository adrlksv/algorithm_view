import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path

def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            RotatingFileHandler(
                log_dir / "app.log",
                maxBytes=1024 * 1024 * 5,  # 5 MB
                backupCount=3
            ),
            logging.StreamHandler()
        ]
    )

    # Увеличиваем логирование для SQLAlchemy
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.INFO)
    