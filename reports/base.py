from abc import ABC, abstractmethod


class BaseReport(ABC):
    @abstractmethod
    def process_line(self, line: str) -> None:
        """Обработка одной строки лога."""
        pass
    
    @abstractmethod
    def merge(self, other: 'BaseReport') -> None:
        """Объединение данных из другого отчета."""
        pass
    
    @abstractmethod
    def format(self) -> str:
        """Форматирование отчета для вывода."""
        pass
    
    @abstractmethod
    def create_new(self) -> 'BaseReport':
        """Создание нового экземпляра этого типа отчета."""
        pass
