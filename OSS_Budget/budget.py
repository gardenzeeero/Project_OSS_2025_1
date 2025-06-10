import datetime
from expense import Expense

class Budget:
    def __init__(self):
        self.expenses = []

    def add_expense(self, category, description, amount, reflection_score):
        today = datetime.date.today().isoformat()
        expense = Expense(today, category, description, amount, reflection_score)
        self.expenses.append(expense)
        print("지출이 추가되었습니다.\n")

    def list_expenses(self):
        if not self.expenses:
            print("지출 내역이 없습니다.\n")
            return
        print("\n[지출 목록]")
        for idx, e in enumerate(self.expenses, 1):
            print(f"{idx}. {e}")
        print()

    def total_spent(self):
        total = sum(e.amount for e in self.expenses)
        print(f"총 지출: {total}원\n")

    def reflection_summary(self):
        if not self.expenses:
            print("지출 내역이 없습니다.\n")
            return
        
        print("\n[반성 점수 요약]")
        total_reflection = sum(e.reflection_score for e in self.expenses)
        avg_reflection = total_reflection / len(self.expenses)
        
        print(f"총 반성 점수: {total_reflection}점")
        print(f"평균 반성 점수: {avg_reflection:.1f}점")
        print(f"지출 건수: {len(self.expenses)}건")
        
        # 반성 점수별 분포
        score_counts = {}
        for e in self.expenses:
            score = e.reflection_score
            score_counts[score] = score_counts.get(score, 0) + 1
        
        print("\n[점수별 분포]")
        for score in sorted(score_counts.keys()):
            print(f"{score}점: {score_counts[score]}건")
        

        high_reflection = sorted(self.expenses, key=lambda x: x.reflection_score, reverse=True)[:3]
        print("\n[가장 후회되는 지출 TOP 3]")
        for idx, e in enumerate(high_reflection, 1):
            print(f"{idx}. {e}")
        print()


