"""Тестовый драйвер: обычные и негативные сценарии."""
import os
import tempfile
import unittest
from datetime import date, timedelta

from habit_service import HabitService
from checkin_service import CheckinService
from statistics_service import StatisticsService
from storage_service import StorageService


class HabitTrackerTests(unittest.TestCase):
    def setUp(self):
        self.habits = HabitService()
        self.habit = self.habits.add_habit(
            "Читать", "Читать 10 страниц", "daily", "20:00"
        )
        self.checkins = CheckinService(self.habits)
        self.stats = StatisticsService(self.habits)

    def test_add_habit(self):
        self.assertEqual(self.habit["name"], "Читать")
        self.assertEqual(len(self.habits.list_habits()), 1)

    def test_empty_name_is_rejected(self):
        with self.assertRaises(ValueError):
            self.habits.add_habit("   ")

    def test_invalid_frequency_is_rejected(self):
        with self.assertRaises(ValueError):
            self.habits.add_habit("Спорт", frequency="sometimes")

    def test_checkin_and_note(self):
        day = date(2026, 10, 20)
        entry = self.checkins.mark(self.habit["id"], True, "Сделано", day.isoformat())
        self.assertTrue(entry["completed"])
        self.assertEqual(entry["note"], "Сделано")

    def test_duplicate_day_updates_existing_entry(self):
        day = date(2026, 10, 20).isoformat()
        self.checkins.mark(self.habit["id"], True, day=day)
        self.checkins.mark(self.habit["id"], False, "Изменил отметку", day=day)
        self.assertEqual(len(self.habit["checkins"]), 1)
        self.assertFalse(self.habit["checkins"][0]["completed"])

    def test_missing_habit_is_rejected(self):
        with self.assertRaises(ValueError):
            self.checkins.mark(999, True)

    def test_streaks(self):
        start = date(2026, 10, 18)
        for offset in range(3):
            day = (start + timedelta(days=offset)).isoformat()
            self.checkins.mark(self.habit["id"], True, day=day)
        self.assertEqual(self.stats.best_streak(self.habit["id"]), 3)

    def test_invalid_days_is_rejected(self):
        with self.assertRaises(ValueError):
            self.stats.success_rate(self.habit["id"], days=0)
        with self.assertRaises(ValueError):
            self.stats.success_rate(self.habit["id"], days=-2)

    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "habits.json")
            storage = StorageService(path)
            storage.save(self.habits.habits)
            loaded = storage.load()
            self.assertEqual(loaded[0]["name"], "Читать")

    def test_reminder_skips_completed_habit(self):
        today = date.today().isoformat()
        self.checkins.mark(self.habit["id"], True, day=today)
        storage = StorageService("unused.json")
        self.assertEqual(storage.reminders_for_today(self.habits.habits), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
