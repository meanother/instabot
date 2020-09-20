import logging
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s %(funcName)s %(message)s',
)
log = logging.getLogger(__name__)
