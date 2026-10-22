from datetime import date
from habit_service import HabitService
from checkin_service import CheckinService
from statistics_service import StatisticsService
from storage_service import StorageService


def main():
    storage = StorageService("habits.json")
    habit_service = HabitService(storage.load())
    checkins = CheckinService(habit_service)
    stats = StatisticsService(habit_service)

    while True:
        print("\n=== Трекер привычек ===")
        print("1. Показать привычки")
        print("2. Добавить привычку")
        print("3. Отметить выполнение")
        print("4. Статистика привычки")
        print("5. Напоминания на сегодня")
        print("6. Удалить привычку")
        print("0. Выход")
        choice = input("Выбери действие: ").strip()

        try:
            if choice == "1":
                habits = habit_service.list_habits()
                if not habits:
                    print("Пока привычек нет.")
                for habit in habits:
                    print(f'{habit["id"]}. {habit["name"]} — {habit["description"]}')
            elif choice == "2":
                name = input("Название: ")
                description = input("Описание: ")
                frequency = input("Периодичность (daily/weekly): ").strip().lower() or "daily"
                reminder = input("Время напоминания (например, 19:00; можно пропустить): ")
                habit = habit_service.add_habit(name, description, frequency, reminder)
                storage.save(habit_service.habits)
                print(f'Добавлена привычка №{habit["id"]}.')
            elif choice == "3":
                habit_id = int(input("ID привычки: "))
                status = input("Выполнено? (д/н): ").strip().lower()
                if status not in ("д", "н", "да", "нет"):
                    print("Введи д или н.")
                    continue
                note = input("Заметка (необязательно): ")
                checkins.mark(habit_id, status in ("д", "да"), note)
                storage.save(habit_service.habits)
                print("Отметка сохранена.")
            elif choice == "4":
                habit_id = int(input("ID привычки: "))
                print("Текущий стрик:", stats.current_streak(habit_id))
                print("Лучший стрик:", stats.best_streak(habit_id))
                print("Успешность за 30 дней:", str(stats.success_rate(habit_id)) + "%")
            elif choice == "5":
                for reminder in storage.reminders_for_today(habit_service.habits):
                    print(f'{reminder["time"]} — {reminder["name"]}')
                print("(Это список напоминаний, приложение пока не отправляет push-уведомления.)")
            elif choice == "6":
                habit_id = int(input("ID привычки для удаления: "))
                if habit_service.delete_habit(habit_id):
                    storage.save(habit_service.habits)
                    print("Привычка удалена.")
                else:
                    print("Привычка не найдена.")
            elif choice == "0":
                storage.save(habit_service.habits)
                print("Данные сохранены. Пока!")
                break
            else:
                print("Неизвестная команда.")
        except (ValueError, TypeError) as error:
            print("Ошибка:", error)


if __name__ == "__main__":
    main()
