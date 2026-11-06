import math


def parse_rental(text):
    if not isinstance(text, str):
        return "", 0.0

    parts = text.split(":")

    if len(parts) != 2:
        return "", 0.0

    unit, months = parts
    unit = unit.strip()

    if not unit:
        return "", 0.0

    try:
        months = float(months.strip())

        if not math.isfinite(months) or months < 0:
            return "", 0.0

    except (ValueError, TypeError):
        return "", 0.0

    return unit.title(), months


def duration_average(months_csv):
    if not isinstance(months_csv, str) or not months_csv.strip():
        return 0

    try:
        values = [int(r.strip()) for r in months_csv.split(",")]

        if any(v < 0 for v in values):
            return 0

        return sum(values) // len(values)

    except (ValueError, TypeError, ZeroDivisionError):
        return 0


def payable_rent(text):
    if not isinstance(text, str):
        return 0.0

    parts = text.split("|")

    if len(parts) != 2:
        return 0.0

    try:
        rent = float(parts[0].strip())
        discount = float(parts[1].strip())

        if not math.isfinite(rent) or not math.isfinite(discount):
            return 0.0

        if rent < 0 or discount < 0:
            return 0.0

        total = rent * 1.18 - discount
        return max(total, 0.0)

    except (ValueError, TypeError):
        return 0.0


def main():
    print("==== Running parse_rental ====")
    user_input = input("Enter unit:months (e.g. medium:6): ")
    result = parse_rental(user_input)
    print("Unit and Months:", result)

    print("\n==== Running duration_average ====")
    user_input = input("Enter rental months as CSV (e.g. 3,6,12): ")
    result = duration_average(user_input)
    print("Average Duration:", result)

    print("\n==== Running payable_rent ====")
    user_input = input("Enter rent|discount (e.g. 2400|200): ")
    result = payable_rent(user_input)
    print("Payable Rent:", result)


if __name__ == "__main__":
    main()