class ReceiptModule:
    def format_receipt(self, items, tax=0.20):
        if not items:
            raise ValueError("Чек пустой")

        total = 0
        lines = ["FOODCAMPUS - ЧЕК", "-" * 25]

        for item in items:
            name = item["name"]
            price = float(item["price"])
            count = int(item["count"])

            if price < 0 or count <= 0:
                raise ValueError("Неверная цена или количество")

            cost = round(price * count, 2)
            total += cost
            lines.append(f"{name}: {count} x {price:.2f} = {cost:.2f} руб.")

        tax_sum = round(total * tax, 2)
        result = round(total + tax_sum, 2)

        lines.append("-" * 25)
        lines.append(f"Сумма: {total:.2f} руб.")
        lines.append(f"Налог: {tax_sum:.2f} руб.")
        lines.append(f"Итого: {result:.2f} руб.")

        return "\n".join(lines)
