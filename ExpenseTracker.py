import json
from datetime import date, timedelta

import User
from User import User

class ExpenseTracker:
    def __init__(self):
        self.user = User()

    def add_allowance(self):
        while True:
            try:
                print("\n=====ALLOWANCE=====")
                amount = float(input("Enter Allowance: ₱"))
                break
            except ValueError:
                print("Invalid input! Please try again with only valid numbers")
        self.user.current_allowance = self.user.current_allowance + amount
        print(f"Allowance added! Current Allowance: ₱{self.user.current_allowance:,.2f}")



    def add_expense(self):
        while True:
            try:
                print("\n=====EXPENSE=====")
                amount = float(input("Add Expense: ₱"))
                break
            except ValueError:
                print("Invalid input! Please try again with only valid numbers")
        self.user.current_allowance = self.user.current_allowance - amount
        note = input("Enter your note (Optional): ")
        entry = {
            "date": str(date.today()),
            "category": self.choose_category(),
            "note": note,
            "amount": amount,
        }
        self.user.expense_list.append(entry)
        print(f"\nExpense Recorded! Remaining Allowance: ₱{self.user.current_allowance:,.2f}")


    def choose_category(self):
        print("Categories:")
        for index, category in enumerate(self.user.categories):
            print(index + 1, category)

        while True:
            try:
                choice = int(input("Choose a category number: "))
                selected_category = self.user.categories[choice - 1]
                break
            except ValueError:
                print("Invalid input! Please try again with a valid number")
            except IndexError:
                print("Please enter a valid option!")

        if selected_category == "Others":
            custom = input("Enter your new category name: ")
            self.user.categories.insert(-1, custom)
            selected_category = custom
        return selected_category

    # def add_category(self):
    #     new_category = input("Enter new category name: ")
    #     self.categories.append(new_category)
    #     print(f"{new_category} has been added to your categories.")

    def view_summary(self):
        period = input("View summary for the (day/week): ")

        if period == "day":
            category_totals = {}
            for entry in self.user.expense_list:
                if entry["date"] == str(date.today()):
                    cat = entry["category"]
                    if cat not in category_totals:
                        category_totals[cat] = 0
                    category_totals[cat] = category_totals[cat] + entry["amount"]

            print("\n=====SUMMARY=====")
            print("Today's spending by category:")
            for cat, amt in category_totals.items():
                print(f"  {cat}: {amt}")
            print(f"Remaining allowance: {self.user.current_allowance}")

        else:
            monday_date = date.today() - timedelta(days=date.today().weekday())
            print("\n=====WEEKLY BREAKDOWN=====")

            for i in range(7):
                current_day = monday_date + timedelta(days=i)
                day_name = current_day.strftime("%A")
                day_str = str(current_day)
                print(f"\n{day_name} ({day_str}):")
                found_any = False

                for entry in self.user.expense_list:
                    if entry["date"] == day_str:
                        print(f"  {entry['category']}: {entry['amount']} ({entry['note']})")
                        found_any = True
                if not found_any:
                    print("  No expenses")

    def save_expense(self):
        try:
            with open("expense.json", "w") as file:
                save = {
                    "expenses": self.user.expense_list
                }
                json.dump(save, file, indent=4)
        except Exception as e:
            print(f"Failed to save: {e}")

    def get_category_totals(self, start_date, end_date):
        category_totals = {}
        total = 0
        for entry in self.user.expense_list:
            if start_date <= entry["date"] <= end_date:
                cat = entry["category"]
                if cat not in category_totals:
                    category_totals[cat] = 0
                category_totals[cat] = category_totals[cat] + entry["amount"]
                total = total + entry["amount"]
        return category_totals, total


    def compare_periods(self):
        period = input("Compare by (day/week): ")

        if period == "day":
            date1 = input("Enter first date (YYYY-MM-DD): ")
            date2 = input("Enter second date (YYYY-MM-DD): ")

            totals1, total1 = self.get_category_totals(date1, date1)
            totals2, total2 = self.get_category_totals(date2, date2)

            print(f"\n{date1}:")
            for cat, amt in totals1.items():
                print(f"  {cat}: {amt}")
            print(f"  Total: {total1}")

            print(f"\n{date2}:")
            for cat, amt in totals2.items():
                print(f"  {cat}: {amt}")
            print(f"  Total: {total2}")

        else:
            this_monday = date.today() - timedelta(days=date.today().weekday())
            this_sunday = this_monday + timedelta(days=6)
            last_monday = this_monday - timedelta(days=7)
            last_sunday = this_sunday - timedelta(days=7)

            totals1, total1 = self.get_category_totals(str(this_monday), str(this_sunday))
            totals2, total2 = self.get_category_totals(str(last_monday), str(last_sunday))

            print(f"\nThis week ({this_monday} to {this_sunday}):")
            for cat, amt in totals1.items():
                print(f"  {cat}: {amt}")
            print(f"  Total: {total1}")

            print(f"\nLast week ({last_monday} to {last_sunday}):")
            for cat, amt in totals2.items():
                print(f"  {cat}: {amt}")
            print(f"  Total: {total2}")


class Main:
    def __init__(self):
        self.tracker = ExpenseTracker()

    def run(self):
        while True:
            print("\nWelcome to the Expense Track App")
            print("1. Add Allowance")
            print("2. Add Expense")
            print("3. View Summary")
            print("4. Save Expenses")
            print("5. Compare Periods")
            print("6. Exit")

            choice = input("\nEnter your choice: ")
            if choice == "1":
                self.tracker.add_allowance()
            elif choice == "2":
                self.tracker.add_expense()
            elif choice == "3":
                self.tracker.view_summary()
            elif choice == "4":
                self.tracker.save_expense()
            elif choice == "5":
                self.tracker.compare_periods()
            elif choice == "6":
                break
            else:
                print("Invalid choice, please try again")

main = Main()
main.run()
