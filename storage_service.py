import json
import os
from datetime import date


class StorageService:
    """Сохранение привычек и настройка простых напоминаний."""

    def __init__(self, filename="habits.json"):
        self.filename = filename

    def save(self, habits):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(habits, file, ensure_ascii=False, indent=2)

    def load(self):
        if not os.path.exists(self.filename):
            return []
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise ValueError("Файл данных повреждён: проверьте формат JSON.") from error

        if not isinstance(data, list):
            raise ValueError("В файле должен храниться список привычек.")
        return data

    def reminders_for_today(self, habits, now=None):
        """Возвращает список напоминаний; фактические push-уведомления не отправляет."""
        now = now or date.today()
        today = now.isoformat()
        reminders = []
        for habit in habits:
            if habit.get("archived") or not habit.get("reminder_time"):
                continue
            completed_today = any(
                item.get("date") == today and item.get("completed") is True
                for item in habit.get("checkins", [])
            )
            if not completed_today:
                reminders.append({
                    "habit_id": habit["id"],
                    "name": habit["name"],
                    "time": habit["reminder_time"]
                })
        return reminders
