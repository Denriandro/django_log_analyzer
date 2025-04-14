from typing import Dict, Type, List

from reports.base import BaseReport
from reports.handlers import HandlersReport


# Реестр доступных отчетов
_REPORT_REGISTRY: Dict[str, Type[BaseReport]] = {
    "handlers": HandlersReport,
    # сюда добавлять новые отчёты
}


def get_report_class(report_name: str) -> Type[BaseReport]:
    """Получает класс отчета по имени."""
    return _REPORT_REGISTRY.get(report_name.lower())


def get_available_reports() -> List[str]:
    """Получает список доступных названий отчетов."""
    return list(_REPORT_REGISTRY.keys())
