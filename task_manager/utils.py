from datetime import datetime as dt
from enum import Enum

FEATURES = {
    'title': 'Название',
    'description': 'Описание',
    'category': 'Категория',
    'due_date': 'Срок выполнения',
    'priority': 'Приоритет',
    'status': 'Статус задачи'
}


class Priority(Enum):
    HIGH = 'Высокий'
    MEDIUM = 'Средний'
    LOW = 'Низкий'


class Status(Enum):
    COMPLETED = 'Выполнена'
    UNCOMPLETED = 'Не выполнена'


def validate_date(date: str) -> dt:
    try:
        parsed_date = dt.strptime(date, "%Y-%m-%d")
        today = dt.now().date()
        if parsed_date.date() < today:
            raise ValueError("The due date must be today or a future date.")
        return parsed_date
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")