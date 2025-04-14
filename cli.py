import argparse
from pathlib import Path
from typing import List, Dict, Any

from analyzer import LogAnalyzer
from reports import get_report_class, get_available_reports


def validate_files(file_paths: List[str]) -> List[Path]:
    """Проверяет, что файлы существуют и доступны для чтения."""

    valid_files = []
    for file_path in file_paths:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        if not path.is_file():
            raise ValueError(f"Неверный путь: {file_path}")
        valid_files.append(path)
    return valid_files


def parse_args() -> Dict[str, Any]:
    """Парсит аргументы командной строки."""

    parser = argparse.ArgumentParser(
        description="Анализ логов Django и создание отчета."
    )
    parser.add_argument(
        "log_files",
        nargs="+",
        help="Пути к файлам логов для анализа"
    )
    parser.add_argument(
        "--report",
        required=False,
        help="Название отчета"
    )
    return vars(parser.parse_args())


def main():
    """Основная точка входа."""

    try:
        args = parse_args()
        log_files = validate_files(args["log_files"])

        report_class = get_report_class(args["report"])
        if report_class is None:
            available_reports = ", ".join(get_available_reports())
            raise ValueError(
                f"Unknown report: {args['report']}."
                f" Available reports: {available_reports}"
            )

        analyzer = LogAnalyzer(report_class())
        results = analyzer.analyze_files(log_files)
        print(results.format())

    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
