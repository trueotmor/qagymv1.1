import json
from pathlib import Path
from typing import Any, Dict

def load_payload(module: str, payload_name: str, dynamic_values) -> Dict[str, Any]:
    """
    Загружает payload из JSON-файла.
    
    Args:
        module: Папка модуля (например, 'auth' или 'users').
        payload_name: Имя файла без расширения (например, 'login_valid').

    Returns:
        Словарь c данными из JSON.
    
    Raises:
        FileNotFoundError: Если файл не существует.
    """
    payload_dir = Path(__file__).parent / "payloads" / module
    file_path = payload_dir / f"{payload_name}.json"
    
    if not file_path.exists():
        raise FileNotFoundError(f"Payload file not found: {file_path}")
    
    with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

    if dynamic_values:
        for key, value in dynamic_values.items():
            if key not in data:
                 raise KeyError(f"Key '{key}' not found in JSON payload!")
            data[key] = value
    return data    
    
    

# def load_expected_response(module: str, scenario: str) -> Dict[str, Any]:
#     """
#     Загружает ожидаемый ответ API для негативного сценария.
#     """
#     return load_payload(module, f"error_responses/{scenario}")