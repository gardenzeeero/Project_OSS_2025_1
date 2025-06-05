import datetime

class ImpulseItem:
    def __init__(self, category, description, amount):
        self.id = datetime.datetime.now().timestamp() # 간단한 고유 ID
        self.category = category
        self.description = description
        self.amount = amount
        self.added_date = datetime.date.today().isoformat()
        self.status = "pending"
    def __str__(self):
        return f"[{self.added_date}] ({self.status}) {self.category} - {self.description}: {self.amount}원" 