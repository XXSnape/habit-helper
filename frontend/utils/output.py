from datetime import datetime, timedelta

from utils.cache_keys import HABITS_KEY


def present_data(data: dict, initial_text="") -> str:
    """
    Переводит данные из словаря в понятный для пользователя текст
    :param data: данные для пользователя
    :param initial_text: текст в начале сообщения пользователю
    :return: текст для отправки пользователю
    """
    return f"<b>{initial_text}</b>\n\n" + "\n\n".join(
        f"<b><i><u>{key}</u></i></b>: {value}" for key, value in data.items()
    )


def get_format_datetime(date_and_time: str) -> str:
    """
    Переводит дату и время в читаемый для пользователя вид
    :param date_and_time: дата и время
    :return: дата и время для отображения пользователю
    """
    return (
        datetime.strptime(date_and_time, "%Y-%m-%dT%H:%M:%S.%f") + timedelta(hours=3)
    ).strftime("%d.%m.%Y %H:%M")


def get_format_hour(hour: int) -> str:
    """
    Создает строку вида HH:00
    :param hour: час
    :return: строка вида HH:00
    """
    return f"{str(hour).zfill(2)}:00"


def get_my_info_from_json(data: dict) -> str:
    """
    Формирует информацию о пользователе из кэша
    :param data: кэш
    :return: данные пользователя
    """
    date_of_registration = get_format_datetime(data["date_of_registration"])

    information = {
        "Никнейм": data["username"],
        "Активен": "Да" if data["is_active"] else "Нет",
        "Дата и время регистрации": date_of_registration,
    }
    return present_data(information, initial_text="Информация о вас:")


def get_text_from_cache(cache: dict) -> str | None:
    """
    Формирует информацию о привычках пользователя из кэша
    :param cache: кэш
    :return: данные о привычках или None, если их нет
    """
    text = (
        "Чтобы посмотреть детальную информацию о привычке, просто введите её номер\n\n"
    )
    if len(cache[HABITS_KEY]) == 1:
        return None
    for ind, habit in enumerate(cache[HABITS_KEY][1:], 1):
        intermediate_text = (
            f"{ind}) {habit['name']} [{get_format_hour(habit['notification_hour'])}]"
        )
        if habit["is_frozen"]:
            intermediate_text += " (приостановлена)"
        text += f"{intermediate_text}\n"

    return text


def get_habit_details_from_cache(
    cache: dict,
    number: int,
    initial_text: str = "",
) -> str | None:
    """
    Формирует информацию о деталях привычки ппо кэшу
    :param cache: кэш
    :param number: номер привычки в кэше
    :param initial_text: текст в начале сообщения пользователю
    :return: детальная информация о привычке или None, если number нет в кэше
    """
    try:
        habit = cache.get(HABITS_KEY)[number]
    except IndexError:
        return None
    created_at = get_format_datetime(habit["created_at"])
    details = {
        "Название": habit["name"],
        "Время напоминания": get_format_hour(habit["notification_hour"]),
        "Количество дней для формирования привычки": str(habit["count"]),
        "Осталось дней до конца": str(
            (habit["count"] - sum(track["is_done"] for track in habit["tracking"]))
        ),
        "Описание": habit["description"],
        "Приостановлена": "Да" if habit["is_frozen"] else "Нет",
        "Дата и время создания": created_at,
    }
    output = present_data(details, initial_text=initial_text)
    return output


def habit_has_already_been_completed(days: int) -> str:
    """
    Сообщает о том, что действия для формирования привычки были выполнены days дней
    :param days: количество дней
    :return: сообщение пользователю
    """
    return f"Вы уже выполнили действия для формирования привычки {days} дней. Введите число больше"
