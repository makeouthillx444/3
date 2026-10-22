class HabitService:
    """Создание и управление привычками."""

    def __init__(self, habits=None):
        self.habits = habits if habits is not None else []
        self.next_id = max((h.get("id", 0) for h in self.habits), default=0) + 1

    def add_habit(self, name, description="", frequency="daily", reminder_time=""):
        name = str(name).strip()
        if not name:
            raise ValueError("Название привычки не может быть пустым.")
        if frequency not in ("daily", "weekly"):
            raise ValueError("Периодичность должна быть daily или weekly.")

        habit = {
            "id": self.next_id,
            "name": name,
            "description": str(description).strip(),
            "frequency": frequency,
            "reminder_time": str(reminder_time).strip(),
            "archived": False,
            "checkins": []
        }
        self.habits.append(habit)
        self.next_id += 1
        return habit

    def delete_habit(self, habit_id):
        for habit in self.habits:
            if habit["id"] == habit_id:
                self.habits.remove(habit)
                return True
        return False

    def archive_habit(self, habit_id):
        habit = self.get_habit(habit_id)
        if habit is None:
            return False
        habit["archived"] = True
        return True

    def get_habit(self, habit_id):
        for habit in self.habits:
            if habit["id"] == habit_id:
                return habit
        return None

    def list_habits(self, include_archived=False):
        if include_archived:
            return list(self.habits)
        return [habit for habit in self.habits if not habit["archived"]]
