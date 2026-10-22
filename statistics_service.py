from datetime import date, timedelta


class StatisticsService:
    """Расчёт серий и процента выполнения."""

    def __init__(self, habit_service):
        self.habit_service = habit_service

    def _completed_dates(self, habit_id):
        habit = self.habit_service.get_habit(habit_id)
        if habit is None:
            raise ValueError("Привычка не найдена.")
        return {
            item["date"] for item in habit["checkins"]
            if item.get("completed") is True
        }

    def current_streak(self, habit_id, today=None):
        completed = self._completed_dates(habit_id)
        current_day = today or date.today()
        # Если сегодня ещё не отмечено, серия может продолжаться со вчера.
        if current_day.isoformat() not in completed:
            current_day -= timedelta(days=1)

        streak = 0
        while current_day.isoformat() in completed:
            streak += 1
            current_day -= timedelta(days=1)
        return streak

    def best_streak(self, habit_id):
        completed = sorted(date.fromisoformat(item) for item in self._completed_dates(habit_id))
        best = current = 0
        previous = None
        for day in completed:
            if previous is not None and day == previous + timedelta(days=1):
                current += 1
            else:
                current = 1
            best = max(best, current)
            previous = day
        return best

    def success_rate(self, habit_id, days=30, today=None):
        if not isinstance(days, int) or isinstance(days, bool) or days <= 0:
            raise ValueError("Количество дней должно быть положительным целым числом.")
        habit = self.habit_service.get_habit(habit_id)
        if habit is None:
            raise ValueError("Привычка не найдена.")
        end = today or date.today()
        start = end - timedelta(days=days - 1)
        entries = {
            item["date"]: item["completed"]
            for item in habit["checkins"]
            if start.isoformat() <= item["date"] <= end.isoformat()
        }
        completed_count = sum(1 for value in entries.values() if value)
        return round(completed_count / days * 100, 1)
