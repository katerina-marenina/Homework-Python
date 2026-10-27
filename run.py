import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"

sys.path.insert(0, str(SRC_DIR))

from analyze import OrderAnalyzer

def main():
    analyze = OrderAnalyzer()
    stats = analyze.process_all_files()
    
    print("\n" + "=" * 50)
    print("Итог анализа:")
    print("=" * 50)

    print(f"Успешно обработано: {stats['processed']}")
    print(f"Файлов с ошибками: {stats['errors']}")
    print(f"Общее количество файлов:{stats['processed'] + stats['errors']}")
    
    print("=" * 50)
    print("Проверьте папку reports/ и logs/")

if __name__ == "__main__":
    main()
