import json
from pathlib import Path
from typing import Any


def write_to_file(data: dict[str, Any], filename: Path) -> None:
    """
    Записывает данные в файл в формате списка словарей.

    Если файл существует, функция загружает существующие данные, добавляет новый словарь
    и перезаписывает файл с обновленным списком.

    Args:
        data (Dict[str, Any]): Сообщение от клиента, которое нужно записать.
        filename (Path): Путь к файлу, в который будут записаны данные.

    Returns:
        None
    """
    if filename.exists():
        with open(filename, "r", encoding="utf-8") as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    existing_data.append(data)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)
