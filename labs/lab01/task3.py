"""Завдання 3: хешування, CSV-база, JSON-логування (варіант 7)."""

import csv
import functools
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from shared.student import VARIANT_NUMBER

SALT = str(VARIANT_NUMBER).zfill(5)
MIN_LENGTH = 15
HASH_ALGO = "sha384"
DATA_DIR = Path(__file__).parent / "data"
USERS_FILE = DATA_DIR / "users.csv"
LOG_FILE = DATA_DIR / "log.json"


class ValidationError(Exception):
    """Пароль не відповідає вимогам політики."""


def generate_hash(password: str, salt: str = "00000") -> str:
    """Повертає hex-хеш від password + salt."""
    if not password or not salt:
        raise ValueError("Пароль або сіль порожні")
    if len(password) < MIN_LENGTH:
        raise ValidationError(f"Пароль коротший за {MIN_LENGTH} символів")
    data = (password + salt).encode("utf-8")
    return hashlib.new(HASH_ALGO, data).hexdigest()


def write_log(entry: dict) -> None:
    """Додає запис у log.json."""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        logs = []
        if LOG_FILE.exists():
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        logs.append(entry)
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)
    except (PermissionError, OSError, json.JSONDecodeError) as err:
        print(f"[!] Не вдалося записати лог: {err}")


def log_event(func):
    """Декоратор: логує кожну спробу входу (без паролів)."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = "failure"
        try:
            outcome = func(*args, **kwargs)
            result = "success" if outcome else "failure"
            return outcome
        finally:
            username = args[0] if args else kwargs.get("username", "")
            write_log(
                {
                    "event": "login",
                    "user": username,
                    "result": result,
                    "timestamp": datetime.now(UTC).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "args": [
                        a if i == 0 else "***" for i, a in enumerate(args)
                    ],
                    "kwargs": {
                        k: "***" if k == "password" else v
                        for k, v in kwargs.items()
                    },
                }
            )

    return wrapper


def create_user(username, password):
    """Повертає (username, hash)."""
    return username, generate_hash(password, SALT)


def create_users(users_list):
    """Записує користувачів у users.csv."""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(USERS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "password_hash"])
            for username, password in users_list:
                try:
                    writer.writerow(create_user(username, password))
                except (ValueError, ValidationError) as err:
                    print(f"[!] Пропущено '{username}': {err}")
    except (PermissionError, OSError) as err:
        print(f"[!] Помилка запису CSV: {err}")


def read_users_db():
    """Зчитує users.csv у список словників."""
    users_db = []
    try:
        with open(USERS_FILE, "r", encoding="utf-8", newline="") as f:
            users_db.extend(csv.DictReader(f))
    except FileNotFoundError:
        print("[!] Файл бази не знайдено")
    except (PermissionError, OSError) as err:
        print(f"[!] Помилка читання CSV: {err}")
    return users_db


def print_users_db(users_db):
    """Виводить таблицю користувачів."""
    print(f"{'Логін':<20}{'Хеш пароля'}")
    for user in users_db:
        print(f"{user['username']:<20}{user['password_hash']}")


@log_event
def login(username: str, password: str) -> bool:
    """Перевіряє логін і пароль."""
    if not username or not password:
        raise ValueError("Порожній логін або пароль")
    try:
        hashed = generate_hash(password, SALT)
    except ValidationError:
        return False
    return any(
        u["username"] == username and u["password_hash"] == hashed
        for u in read_users_db()
    )


def main():
    """Запуск завдання 3."""
    users_to_register = (
        ("admin_sec", "SecurePassword#2026"),
        ("crypto_ivan", "Network#Defender2026"),
        ("guest_user", "weak"),
        ("analyst_olga", "Firewall@Rules!2026"),
        ("sec_expert", "Incident$Response77"),
        ("test_user_1", "Short1!"),
        ("auditor_petro", "Audit#Trail!Secure9"),
        ("dev_oleh", "Python&Hashing2026!"),
        ("net_admin", "Router!Switch#Admin1"),
        ("user_empty", ""),
    )
    create_users(users_to_register)

    print("\nБАЗА ДАНИХ (CSV):")
    print_users_db(read_users_db())

    print("\nПЕРЕВІРКА ВХОДУ:")
    print("admin_sec:", login("admin_sec", "SecurePassword#2026"))
    print(
        "crypto_ivan (невірний пароль):",
        login("crypto_ivan", "wrong"),
    )
    try:
        login("", "")
    except ValueError as err:
        print("Порожні дані:", err)


if __name__ == "__main__":
    main()
