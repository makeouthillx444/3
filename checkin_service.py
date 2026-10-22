from datetime import date


class CheckinService:
    """Ежедневные отметки выполнения привычек."""

    def __init__(self, habit_service):
        self.habit_service = habit_service

    def mark(self, habit_id, completed=True, note="", day=None):
        habit = self.habit_service.get_habit(habit_id)
        if habit is None:
            raise ValueError("Привычка не найдена.")
        if habit["archived"]:
            raise ValueError("Нельзя отмечать архивную привычку.")
        if not isinstance(completed, bool):
            raise TypeError("Статус должен быть True или False.")

        day = day or date.today().isoformat()
        # Одна отметка на привычку за один день: новая заменяет старую.
        for entry in habit["checkins"]:
            if entry["date"] == day:
                entry.update({"completed": completed, "note": str(note).strip()})
                return entry

        entry = {"date": day, "completed": completed, "note": str(note).strip()}
        habit["checkins"].append(entry)
        habit["checkins"].sort(key=lambda item: item["date"])
        return entry

    def get_day_entries(self, day=None):
        day = day or date.today().isoformat()
        result = []
        for habit in self.habit_service.list_habits():
            for entry in habit["checkins"]:
                if entry["date"] == day:
                    result.append({"habit_id": habit["id"], "habit_name": habit["name"], **entry})
        return result
