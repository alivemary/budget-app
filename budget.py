import math


class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = list()

    def __str__(self):
        def format_amount(amount):
            return f"{amount:.2f}"

        title = self.name.center(30, "*")
        inventory = "\n".join(
            [
                f"{item['description'][:23].ljust(23)}{format_amount(item['amount']).rjust(7)}"
                for item in self.ledger
            ]
        )
        total = f"Total: {self.get_balance()}"
        return "\n".join([title, inventory, total])

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if not self.check_funds(amount):
            return False
        self.deposit(-amount, description)
        return True

    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, target_category):
        if not self.check_funds(amount):
            return False
        self.withdraw(amount, f"Transfer to {target_category.name}")
        target_category.deposit(amount, f"Transfer from {self.name}")
        return True

    def check_funds(self, amount):
        return self.get_balance() >= amount

    def get_withdrawals_amount(self):
        return -sum([item["amount"] for item in self.ledger if item["amount"] < 0])


def create_spend_chart(categories):
    def generate_chart_line(current_percentage, percentages):
        category_chart = "  ".join(
            [
                "o" if percentage >= current_percentage else " "
                for percentage in percentages
            ]
        )
        return f"{str(current_percentage).rjust(3)}| {category_chart}  "

    def generate_name_line(index, names):
        line = " " * 4
        for name in names:
            try:
                line += name[index].center(3)
            except IndexError:
                line += " " * 3

        return line + " "

    title = "Percentage spent by category"
    withdrawal = [category.get_withdrawals_amount() for category in categories]
    spent = sum(withdrawal)
    percentages = [
        int(math.floor((100 * withdraw / spent) / 10.0)) * 10 for withdraw in withdrawal
    ]
    chart = "\n".join(
        [generate_chart_line(line, percentages) for line in range(100, -10, -10)]
    )
    separator = " " * 4 + "-" * (len(categories) * 3 + 1)

    names = [category.name for category in categories]
    maxlen = max([len(name) for name in names])

    names_chart = "\n".join(
        [generate_name_line(index, names) for index in range(maxlen)]
    )

    return "\n".join([title, chart, separator, names_chart])