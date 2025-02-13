from typing import List
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

@dataclass
class OptimizationResult:
    print_order: List[str]
    total_time: int

def optimize_printing(print_jobs: List[PrintJob], constraints: PrinterConstraints) -> OptimizationResult:
    result = OptimizationResult([], 0)

    sorted_jobs = sorted(print_jobs, key=lambda job: (job.priority, -job.volume, job.print_time))

    current_volume = 0
    current_items = 0

    for job in sorted_jobs:
        if current_items < constraints.max_items and current_volume + job.volume <= constraints.max_volume:
            current_volume += job.volume
            current_items += 1
            result.total_time = max(result.total_time, job.print_time)
        else:
            result.total_time += job.print_time
            current_volume = job.volume
            current_items = 1

        result.print_order.append(job.id)

    return result

# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        PrintJob("M1", 100, 1, 120),
        PrintJob("M2", 150, 1, 90),
        PrintJob("M3", 120, 1, 150)
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        PrintJob("M1", 100, 2, 120),  # лабораторна
        PrintJob("M2", 150, 1, 90),  # дипломна
        PrintJob("M3", 120, 3, 150)  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        PrintJob("M1", 250, 1, 180),
        PrintJob("M2", 200, 1, 150),
        PrintJob("M3", 180, 2, 120)
    ]

    constraints = PrinterConstraints(300, 2)

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1.print_order}")
    print(f"Загальний час: {result1.total_time} хвилин")

    print("\\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2.print_order}")
    print(f"Загальний час: {result2.total_time} хвилин")

    print("\\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3.print_order}")
    print(f"Загальний час: {result3.total_time} хвилин")

if __name__ == "__main__":
    test_printing_optimization()
