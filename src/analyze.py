
import sys
import csv
import logging
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import config

#Создание класса OrderAnalyzer - анализ CSV-файлов
class OrderAnalyzer:
    def __init__(self):
#Папки для отчетов
      self.data_dir = Path(config.DATA_DIR)
      self.reports_dir = Path(config.REPORTS_DIR)
      self.logs_dir = Path(config.LOGS_DIR)
      self.reports_dir.mkdir(parents=True, exist_ok=True)
      self.logs_dir.mkdir(parents=True, exist_ok=True)
#Счетчики
      self.processed_files = 0
      self.error_files = 0
#Список с результатами
      self.results = []
#Настройка записи ошибок
      self._setup_logging()

#Настройка логгирования/записи ошибок в файл errors.log
    def _setup_logging(self):
      log_path = self.logs_dir / config.LOG_FILE

      logging.basicConfig(
            filename=log_path,
            level=logging.ERROR,
            format="%(asctime)s - %(levelname)s - %(message)s",
            encoding="utf-8"
        )

      self.logger = logging.getLogger(__name__)

#Загрузка CSV-файла
    def _load_csv(self, file_path):
      try:
        df = pd.read_csv(file_path, low_memory=False)
        if df.empty:
          raise ValueError(f"Файл пуст: {file_path}")

#Проверяем наличиие обязательных колонок
        required_cols = {
          "order_id", 
          "total_amount", 
          config.STATUS_COLUMN
        }
        missing_cols = required_cols - set(df.columns)
        if missing_cols:
          raise ValueError(f"Отсутствуют обязательные колонки: "f"{missing_cols}")
        return df

      except Exception as exc:
        self.logger.error("Ошибка загрузки файла %s: %s", file_path.name, exc)
        return None

#Фильтрация доставленных заказов
    def _filter_delivered(self, df):
        return df[
            df[config.STATUS_COLUMN] == config.DELIVERED_STATUS
        ]

#Расчет метрик
    def _calculate_metrics(self, df):
      delivered = self._filter_delivered(df)

      amounts = pd.to_numeric(delivered["total_amount"], errors="coerce").dropna()
      total_revenue = amounts.sum()
      orders_count = len(amounts)
      avg_check = total_revenue / orders_count if orders_count > 0 else 0.0

      return {
            "total_revenue": float(total_revenue),
            "avg_check": float(avg_check),
            "orders_count": int(orders_count)
        }

#Обработка одного файла
    def process_file(self, file_path):
      df = self._load_csv(file_path)
      if df is None:
        self.error_files += 1
        return
        
      try:
        metrics = self._calculate_metrics(df)
        self.results.append({"file_name": file_path.name, **metrics})

        self.processed_files += 1
        print(f"Обработан: {file_path.name} | "f"Заказов: {metrics['orders_count']} | "f"Выручка: {metrics['total_revenue']:.2f}")

      except Exception as exc:
        self.logger.error("Ошибка обработки файла %s: %s", file_path.name, exc)
        self.error_files += 1

# Обработка всех файлов в папке. Итоговый отчет
    def process_all_files(self):
      csv_files = sorted(self.data_dir.glob("*.csv"))
      print(f"Найдено файлов: {len(csv_files)}")

      for file_path in csv_files:
        self.process_file(file_path)

      if self.results:
        report_path = self.reports_dir / config.OUTPUT_FILE
          
        pd.DataFrame(self.results).to_csv(report_path, index=False, quoting=csv.QUOTE_NONNUMERIC,encoding="utf-8-sig")
        print(f"Отчёт сохранён: {report_path}")

      return {
        "processed": self.processed_files,
        "errors": self.error_files
        }
