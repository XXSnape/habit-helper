from datetime import datetime, timedelta

from utils.constants import HABITS_KEY


def present_data(data: dict, initial_text="") -> str:
    return f"<b>{initial_text}</b>\n\n" + "\n\n".join(
        f"<b><i><u>{key}</u></i></b>: {value}" for key, value in data.items()
    )


def get_format_datetime(date_and_time: str) -> str:
    return (
        datetime.strptime(date_and_time, "%Y-%m-%dT%H:%M:%S.%f") + timedelta(hours=3)
    ).strftime("%d.%m.%Y %H:%M")


def get_my_info_from_json(data: dict) -> str:
    date_of_registration = get_format_datetime(data["date_of_registration"])
    print("d", data)
    information = {
        "Никнейм": data["username"],
        "Активен": "Да" if data["is_active"] else "Нет",
        "Дата и время регистрации": date_of_registration,
    }
    return present_data(information, initial_text="Информация о вас:")


def get_text_from_cache(data: dict) -> str | None:
    text = (
        "Чтобы посмотреть детальную информацию о привычке, просто введите её номер\n\n"
    )
    if len(data[HABITS_KEY]) == 1:
        return None
    for ind, habit in enumerate(data[HABITS_KEY][1:], 1):
        intermediate_text = f"{ind}) {habit['name']}"
        if habit["is_frozen"]:
            intermediate_text += " (приостановлена)"
        text += f"{intermediate_text}\n"

    return text


def get_habit_details_from_cache(
    data: dict,
    number: int,
    initial_text: str = "",
) -> str | None:
    try:
        habit = data.get(HABITS_KEY)[number]
    except IndexError:
        return None
    created_at = get_format_datetime(habit["created_at"])
    details = {
        "Название": habit["name"],
        "Время напоминания": f"{habit['notification_hour']}:00",
        "Количество дней привития": str(habit["count"]),
        "Осталось дней до конца": str((habit["count"] - len(habit["tracking"]))),
        "Описание": habit["description"],
        "Приостановлена": "Да" if habit["is_frozen"] else "Нет",
        "Дата и время создания": created_at,
    }
    output = present_data(details, initial_text=initial_text)
    return output
