from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import logging
from logging.handlers import RotatingFileHandler
import os

# Ensure logs directory exists
if not os.path.exists("logs"):
    os.mkdir("logs")

# Configure root logger
logging.basicConfig(
    level=logging.INFO,  # Default level
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

# Error file handler (writes only ERROR and above)
error_handler = RotatingFileHandler("logs/error.log", maxBytes=1000000, backupCount=5)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
))

# Attach to root logger
logging.getLogger().addHandler(error_handler)

# Use in your routes
logger = logging.getLogger(__name__)
