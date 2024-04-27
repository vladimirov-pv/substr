from dotenv import load_dotenv
import os
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_file_path  = os.path.join(BASE_DIR, ".env")
load_dotenv(env_file_path)

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

logging.basicConfig(level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger(__name__)

REDIS_HOST = os.getenv('REDIS_HOST', '')
REDIS_PORT = os.getenv('REDIS_PORT', 0)
REDIS_DB = os.getenv("REDIS_DB", 0)
CHANNEL_NAME = os.getenv("CHANNEL_NAME", "rules")
