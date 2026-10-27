import csv
import os
from datetime import datetime

FILE_NAME = "transactions.csv"
FIELDNAMES = ["date", "type", "category", "amount"]


def load_transactions():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def add_transaction():
    transaction_type = input(
        "Enter type (income/expense): "
    ).strip().lower()

    if transaction_type not in ("income", "expense"):
        print("Invalid type. Enter income or expense.")
        return

    category = input("Enter category: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    try:
        amount = float(input("Enter amount: "))
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    date = input(
        "Enter date (YYYY-MM-DD), or press Enter for today: "
    ).strip()

    if not date:
        date = datetime.today().strftime("%Y-%m-%d")
    else:
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            return

    needs_header = (
        not os.path.exists(FILE_NAME)
        or os.path.getsize(FILE_NAME) == 0
    )

    with open(FILE_NAME, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)

        if needs_header:
            writer.writeheader()

        writer.writerow({
            "date": date,
            "type": transaction_type,
            "category": category,
            "amount": f"{amount:.2f}",
        })

    print("Transaction added successfully!")


def view_transactions():
    transactions = load_transactions()

    if not transactions:
        print("No transactions found yet.")
        return

    print("\n--- All Transactions ---")
    print(f"{'Date':<12} {'Type':<10} {'Category':<18} {'Amount':>12}")
    print("-" * 56)

    for transaction in transactions:
        print(
            f"{transaction['date']:<12} "
            f"{transaction['type']:<10} "
            f"{transaction['category']:<18} "
            f"{float(transaction['amount']):>12.2f}"
        )


def show_balance():
    transactions = load_transactions()

    income = sum(
        float(t["amount"])
        for t in transactions
        if t["type"] == "income"
    )

    expenses = sum(
        float(t["amount"])
        for t in transactions
        if t["type"] == "expense"
    )

    print("\n--- Balance Summary ---")
    print(f"Total Income:    {income:.2f}")
    print(f"Total Expenses:  {expenses:.2f}")
    print(f"Current Balance: {income - expenses:.2f}")


def main():
    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add Income or Expense")
        print("2. View All Transactions")
        print("3. Show Balance")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transactions()
        elif choice == "3":
            show_balance()
        elif choice == "4":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid choice. Select 1, 2, 3, or 4.")


def run():
    print("Starting Expense Tracker...")
    main()


if __name__ == "__main__":
    run()
