
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
LOGS_DIR = BASE_DIR / "logs"

OUTPUT_FILE = "summary_report.csv"
LOG_FILE = "errors.log"

STATUS_COLUMN = "status"
DELIVERED_STATUS = "Delivered"
