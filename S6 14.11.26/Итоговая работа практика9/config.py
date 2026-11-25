# Настройки проекта
from pathlib import Path

# Папка, в которой находится проект
BASE_DIR = Path(__file__).parent

# Папки с исходными данными и результатами
RAW_DIR = BASE_DIR / "data" / "raw"
RESULT_DIR = BASE_DIR / "data" / "processed"
REPORT_DIR = BASE_DIR / "reports"

# Месяц, за который сравниваем план и факт
ANALYSIS_MONTH = "2025-05"
