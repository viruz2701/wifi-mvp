import re

def validate_phone_number(phone: str) -> bool:
    """
    Проверяет, что номер телефона соответствует международному формату E.164.
    Допускается наличие ведущего знака '+' или его отсутствие.
    Длина номера без плюса должна быть от 7 до 15 цифр.
    """
    # Убираем все нецифровые символы, кроме ведущего плюса
    cleaned = re.sub(r'[^\d+]', '', phone)
    if not cleaned:
        return False
    if cleaned.startswith('+'):
        # После плюса должны идти только цифры, общая длина 8-16 (с плюсом)
        return re.match(r'^\+\d{7,15}$', cleaned) is not None
    else:
        # Без плюса: только цифры, длина 7-15
        return re.match(r'^\d{7,15}$', cleaned) is not None

def normalize_phone_number(phone: str) -> str:
    """
    Приводит номер к единому формату: +XXXXXXXXXXX (без пробелов и дефисов).
    Если номер без плюса, добавляет +.
    """
    # Убираем все кроме цифр
    digits = re.sub(r'\D', '', phone)
    if not digits:
        return ''
    # Если номер начинается с 8, заменяем на +375? Но лучше не предполагать.
    # Просто добавляем +, если его не было
    if phone.startswith('+'):
        return '+' + digits
    else:
        return '+' + digits