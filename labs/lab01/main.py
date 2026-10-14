"""Демонстрація всіх завдань ЛР №1."""

from labs.lab01 import task1, task2, task3


def main():
    """Послідовно запускає завдання 1-3."""
    for module in (task1, task2, task3):
        print("=" * 60)
        module.main()


if __name__ == "__main__":
    main()
