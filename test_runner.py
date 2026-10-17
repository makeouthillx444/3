from receipt import ReceiptModule

receipt = ReceiptModule()

items = [
    {"name": "Борщ", "price": 120, "count": 1},
    {"name": "Котлета с пюре", "price": 180.5, "count": 2},
]

print("Тест 1: обычный чек")
print(receipt.format_receipt(items))

print("\nТест 2: пустой список")
try:
    receipt.format_receipt([])
except ValueError as error:
    print("Ошибка обработана:", error)

print("\nТест 3: отрицательная цена")
try:
    receipt.format_receipt([
        {"name": "Суп", "price": -50, "count": 1}
    ])
except ValueError as error:
    print("Ошибка обработана:", error)

print("\nТест 4: текст вместо цены")
try:
    receipt.format_receipt([
        {"name": "Суп", "price": "abc", "count": 1}
    ])
except ValueError:
    print("Ошибка: цена должна быть числом")
