"""Завдання 1: аналізатор надійності паролів (варіант 7)."""

import random

from shared.student import STUDENT_NAME, VARIANT_NUMBER


def evaluate_password(password, all_passwords, criteria, forbidden):
    """Повертає рівень надійності пароля."""
    min_len = criteria["min_length"]
    if password in forbidden or len(password) < min_len:
        return "Заборонений"

    checks = [
        any(c.isdigit() for c in password),
        any(c.isupper() for c in password),
        any(not c.isalnum() for c in password),
    ]
    satisfied = sum(checks)

    if satisfied == len(checks):
        unique = all_passwords.count(password) == 1
        if len(password) >= min_len + 4 and unique:
            return "Дуже сильний"
        return "Сильний"
    if satisfied > 0:
        return "Середній"
    return "Слабкий"


def main():
    """Запуск завдання 1."""
    print(f"{STUDENT_NAME}, варіант {VARIANT_NUMBER}\n")
    passwords = [
        "NetworkS3c!",
        "easy",
        "Firewa11@Pass",
        "anonymous",
        "Intrus10n#Detect",
        "sample",
        "Malwar3@Scan",
        "qwerty",
        "Vulnerab1l!ty",
        "common",
    ]
    criteria = {
        "min_length": 9,
        "require_digits": True,
        "require_upper": True,
        "require_special": True,
    }
    forbidden = {
        "easy",
        "anonymous",
        "sample",
        "qwerty",
        "common",
        "password",
    }

    indices = [random.randrange(len(passwords)) for _ in range(3)]
    duplicates = [passwords[i] for i in indices]
    passwords.extend(duplicates)
    print("Індекси дублювання:", indices, "\n")

    print(f"{'Пароль':<20}{'Довжина':<10}{'Рівень надійності'}")
    print("-" * 50)
    for pw in passwords:
        level = evaluate_password(pw, passwords, criteria, forbidden)
        print(f"{pw:<20}{len(pw):<10}{level}")


if __name__ == "__main__":
    main()
