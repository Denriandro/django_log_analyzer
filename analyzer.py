from multiprocessing import Pool, cpu_count
from pathlib import Path
from typing import List

from reports import BaseReport


class LogAnalyzer:
    def __init__(self, report: BaseReport):
        self.report = report

    def analyze_files(self, file_paths: List[Path]) -> BaseReport:
        """
        Анализ нескольких файлов журналов и объединение результатов.

        Принимает:
            file_paths: Список путей к файлам логов
            
        Возвращает:
            BaseReport: Объект отчета с объединенными данными
        """

        with Pool(processes=cpu_count()) as pool:
            results = pool.map(self._process_single_file, file_paths)
        
        for result in results:
            self.report.merge(result)

        return self.report

    def _process_single_file(self, file_path: Path) -> BaseReport:
        """
        Обработка одного файла логов.
        
        Принимает:
            file_path: Путь к файлу логов
            
        Возвращает:
            BaseReport: Объект отчета с данными из этого файла
        """
        report = self.report.create_new()
        
        with file_path.open('r', encoding='utf-8') as f:
            for line in f:
                report.process_line(line)
                
        return report
