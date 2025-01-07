from pathlib import Path
import sys
from loguru import logger


PROJ_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJ_ROOT / "data"
LOG_DIR = PROJ_ROOT / "logs"

logger.add(LOG_DIR / "file.log", level='INFO')
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

API_URL = "https://ebolig.nordea.dk/wemapp/api/credit/fixedrate/bonds.json"

T0 = 1735947549.160262
