class Expense:
    def __init__(self, date, category, description, amount, reflection_score):
        self.date = date
        self.category = category
        self.description = description
        self.amount = amount
        self.reflection_score = reflection_score

    def __str__(self):
        return f"[{self.date}] {self.category} - {self.description}: {self.amount}원 (반성점수: {self.reflection_score})"