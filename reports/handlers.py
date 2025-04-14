from collections import defaultdict
from functools import partial
from typing import DefaultDict

from reports import BaseReport


class HandlersReport(BaseReport):
    def __init__(self):
        self.data: DefaultDict[str, DefaultDict[str, int]] = defaultdict(
            partial(defaultdict, int)
        )
        self.levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        self.total_requests = 0

    def process_line(self, line: str) -> None:
        """Обрабатывает строку лога для записей django.requests."""

        if "django.request" not in line:
            return

        try:
            parts = line.split()

            level = parts[2] if len(parts) > 2 else "UNKNOWN"

            method_pos = None
            for i, part in enumerate(parts):
                if part in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                    method_pos = i
                    break

            if method_pos is not None and len(parts) > method_pos + 1:
                handler = parts[method_pos + 1].split('?')[0]

                self.data[handler][level] += 1
                self.total_requests += 1

        except Exception:
            pass

    def merge(self, other: 'HandlersReport') -> None:
        """Объединяет данные из другого отчета HandlersReport."""

        for handler, counts in other.data.items():
            for level, count in counts.items():
                self.data[handler][level] += count
        self.total_requests += other.total_requests

    def format(self) -> str:
        """Форматирует отчет для вывода в консоль."""

        handler_width = max(len("HANDLER"),
                            max(len(handler) for handler in self.data.keys()))

        # Фиксированная ширина для уровней логирования
        level_width = 10

        header = f"{'HANDLER':<{handler_width}}  " + "  ".join(
            f"{level:<{level_width}}" for level in self.levels
        )

        separator = "-" * (
                    handler_width + 2 + len(self.levels) * (level_width + 2))

        rows = []
        for handler in sorted(self.data.keys()):
            row = f"{handler:<{handler_width}}  " + "  ".join(
                f"{self.data[handler].get(level, 0):<{level_width}}"
                for level in self.levels
            )
            rows.append(row)
        rows_str = '\n\n'.join(rows) + '\n\n'

        totals = " " * handler_width + "  " + "  ".join(
            f"{sum(counts.get(level, 0) for counts in self.data.values()):<{level_width}}"
            for level in self.levels
        )

        return (
                f"Total requests: {self.total_requests}\n\n"
                f"{header}\n"
                f"{separator}\n"
                f"{rows_str}"
                f"{totals}"
        )

    def create_new(self) -> 'HandlersReport':
        """Создаёт новый экземпляр HandlersReport."""
        return HandlersReport()
