import datetime
import random
from impulse_item import ImpulseItem
# from expense import Expense # ImpulseControl은 직접 Expense를 만들지 않으므로 주석 처리 또는 삭제

class ImpulseControl:
    def __init__(self):
        self.impulse_items = []
        self.user_points = 0
        self.last_execution_room_penalty_time = None

    def add_to_impulse_calm_room(self, category, description, amount):
        item = ImpulseItem(category, description, amount)
        self.impulse_items.append(item)
        
        earned_points = int(amount * 0.1)
        self.user_points += earned_points

        print(f"\n'{description}' 이(가) 충동소비 진정실에 등록되었습니다.")
        print(f"포인트 +{earned_points}P (총: {self.user_points}P)\n")

    def view_impulse_calm_room(self):
        if not self.impulse_items:
            print("충동소비 진정실에 등록된 항목이 없습니다.\n")
            return
        
        pending_items = [item for item in self.impulse_items if item.status == 'pending']
        if not pending_items:
            print("현재 진정실에 보관 중인 (구매 가능한) 충동 소비 항목이 없습니다.\n")
            return

        print("\n[충동소비 진정실 목록 (보류 중)]")
        for idx, item in enumerate(pending_items, 1):
            print(f"{idx}. {item.category} - {item.description}: {item.amount}원")
        print()

    def view_points(self):
        if self.user_points == 0:
            print("\n현재 보유 포인트가 없습니다. 먼저 충동소비를 진정실에 등록하여 포인트를 쌓아보세요!\n")
        else:
            print(f"\n현재 보유 포인트: {self.user_points}P\n")
        return self.user_points

    def _can_enter_execution_room(self):
        if self.last_execution_room_penalty_time:
            time_since_penalty = datetime.datetime.now() - self.last_execution_room_penalty_time
            if time_since_penalty < datetime.timedelta(hours=24):
                remaining_time = datetime.timedelta(hours=24) - time_since_penalty
                hours, remainder = divmod(remaining_time.total_seconds(), 3600)
                minutes, _ = divmod(remainder, 60)
                print(f"충동소비 실행실은 24시간 후에 입장이 가능합니다.")
                print(f"남은 시간: 약 {int(hours)}시간 {int(minutes)}분\n")
                return False
        return True

    def execute_impulse_item(self, points_to_spend, budget_obj):
        if not self._can_enter_execution_room():
            return False

        if self.user_points == 0:
            print("아이템을 뽑으려면 포인트가 필요합니다. 충동소비를 진정실에 등록해 포인트를 모아주세요.\n")
            return False
        
        if points_to_spend <= 0:
            print("사용할 포인트는 0보다 커야 합니다.\n")
            return False

        if self.user_points < points_to_spend:
            print(f"보유 포인트({self.user_points}P)가 사용하려는 포인트({points_to_spend}P)보다 적습니다.\n")
            return False

        eligible_items = [item for item in self.impulse_items if item.status == 'pending' and item.amount <= points_to_spend]

        if not eligible_items:
            print(f"{points_to_spend}P 이하로 구매 가능한 충동소비 항목이 진정실에 없습니다.\n")
            return False

        print(f"{points_to_spend}P를 사용하여 아이템을 뽑습니다...\n")
        selected_item = random.choice(eligible_items)
        
        print(f"⭐️⭐️⭐️⭐️⭐️⭐️짠!⭐️⭐️⭐️⭐️⭐️⭐️ 충동구매 아이템을 뽑았습니다!!\n")
        print(f"- 카테고리: {selected_item.category}")
        print(f"- 설    명: {selected_item.description}")
        print(f"- 금    액: {selected_item.amount}원 (수락 시 이 금액이 포인트에서 차감됩니다)")
        
        while True:
            choice = input(f"\n'{selected_item.description}'을(를) {selected_item.amount}P로 구매하시겠습니까? (y/n): ").lower()
            if choice == 'y':
                if self.user_points < selected_item.amount:
                    print("오류: 보유 포인트가 상품 금액보다 부족합니다. 상황이 변경되었을 수 있습니다.\n")
                    return False
                
                self.user_points -= selected_item.amount
                selected_item.status = 'purchased'
                
                budget_obj.add_expense(
                    selected_item.category, 
                    f"[충동구매] {selected_item.description}", 
                    selected_item.amount, 
                    datetime.datetime.now()
                )
                print(f"\n🎉 '{selected_item.description}' 구매 완료! 🎉")
                print(f"지출 내역에 추가되었습니다. 남은 포인트: {self.user_points}P\n")
                self.last_execution_room_penalty_time = None 
                return True
            elif choice == 'n':
                print("구매하지 않으셨습니다. 포인트는 그대로 유지됩니다.")
                print("24시간 동안 충동소비 실행실 입장이 제한됩니다.\n")
                self.last_execution_room_penalty_time = datetime.datetime.now()
                return False
            else:
                print("잘못된 입력입니다. y 또는 n으로 답해주세요.") 