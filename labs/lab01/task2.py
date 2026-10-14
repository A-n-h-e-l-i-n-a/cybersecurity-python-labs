"""Завдання 2: система контролю доступу (варіант 7)."""

USERS = {
    "incident_commander": {
        "role": "incident_response",
        "clearance": 4,
        "department": "CSIRT",
        "active": True,
    },
    "malware_analyst": {
        "role": "malware_researcher",
        "clearance": 3,
        "department": "Research",
        "active": True,
    },
    "monitoring_tech": {
        "role": "monitoring",
        "clearance": 2,
        "department": "NOC",
        "active": True,
    },
    "customer_rep": {
        "role": "customer_service",
        "clearance": 1,
        "department": "Customer",
        "active": True,
    },
    "backup_service": {
        "role": "service_account",
        "clearance": 2,
        "department": "System",
        "active": False,
    },
}
RESOURCES = [
    ("incident_playbook", 4),
    ("malware_lab", 3),
    ("monitoring_dashboards", 2),
    ("customer_portal", 1),
    ("emergency_procedures", 4),
    ("service_desk", 1),
    ("reverse_engineering", 3),
    ("alert_systems", 2),
    ("escalation_matrix", 3),
    ("knowledge_base", 1),
]
SECURITY_LEVELS = (
    "Public Access",
    "Authorized",
    "Privileged",
    "Critical",
)
BLOCKED_USERS = {"backup_service", "deactivated_svc", "policy_violation"}


def show_resources():
    """Виводить ресурси з текстовими рівнями безпеки."""
    print("РЕСУРСИ СИСТЕМИ:")
    for name, level in RESOURCES:
        print(f"Ресурс: {name} | Рівень: {SECURITY_LEVELS[level - 1]}")


def check_access(username, resource_level):
    """Повертає рядок з рішенням ALLOW / DENY (причина)."""
    user = USERS.get(username)
    if user is None:
        return "DENY (User not found)"
    if username in BLOCKED_USERS:
        return "DENY (User is blocked)"
    if not user["active"]:
        return "DENY (Account inactive)"
    if user["clearance"] >= resource_level:
        return "ALLOW"
    return "DENY (Insufficient clearance)"


def main():
    """Запуск завдання 2."""
    show_resources()
    print("\nРЕЗУЛЬТАТИ ПЕРЕВІРКИ:")
    for username in sorted(set(USERS) | BLOCKED_USERS):
        for name, level in RESOURCES:
            result = check_access(username, level)
            print(f"user={username} resource={name} -> {result}")


if __name__ == "__main__":
    main()
