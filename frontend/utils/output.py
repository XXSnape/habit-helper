from datetime import datetime

from utils.constants import TEXT_KEY


def present_data(data: dict) -> str:
    return "\n\n".join(
        f"<b><i><u>{key}</u></i></b>: {value}" for key, value in data.items()
    )


def get_text_and_fill_in_cache(json: dict, data: dict) -> str:
    text = (
        "Чтобы посмотреть детальную информацию о привычке, просто введите её номер\n\n"
    )
    for ind, habit in enumerate(json, 1):
        data[str(ind)] = habit
        intermediate_text = f"{ind}) {habit['name']}"
        if habit["is_frozen"]:
            intermediate_text += " (приостановлена)"
        text += f"{intermediate_text}\n"
    data[TEXT_KEY] = text
    return text


def get_habit_details_from_cache(data: dict, number: str) -> str | None:
    habit = data.get(number)
    if habit is None:
        return None
    if isinstance(habit, str):
        return habit
    created_at = datetime.strptime(
        habit["created_at"], "%Y-%m-%dT%H:%M:%S.%f"
    ).strftime("%d.%m.%Y %H:%M")
    details = {
        "Название": habit["name"],
        "Время напоминания": f"{habit['notification_hour']}:00",
        "Количество дней привития": str(habit["count"]),
        "Осталось дней до конца": str((habit["count"] - len(habit["tracking"]))),
        "Описание": habit["description"],
        "Приостановлена": "Да" if habit["is_frozen"] else "Нет",
        "Дата и время создания": created_at,
    }
    output = present_data(details)
    data[number] = output
    return output
