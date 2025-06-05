from budget import Budget
from impulse_control import ImpulseControl


def main():
    budget = Budget()
    impulse_controller = ImpulseControl()

    while True:
        print("\n==== 간단 가계부 (충동소비 관리 시스템 탑재!) ====")
        print("1. 지출 추가")
        print("2. 지출 목록 보기")
        print("3. 총 지출 보기")
        print("--- 충동소비 관리 ---")
        print("4. 충동소비 진정실에 등록 (포인트 적립!)")
        print("5. 충동소비 진정실 목록 보기")
        print("6. 충동소비 실행실 입장 (아이템 뽑기!)")
        print("7. 내 포인트 확인하기")
        print("---------------------")
        print("8. 종료")
        choice = input("선택 > ")

        if choice == "1":
            category = input("카테고리 (예: 식비, 교통 등): ")
            description = input("설명: ")
            try:
                amount = int(input("금액(원): "))
                if amount <= 0:
                    print("금액은 0보다 커야 합니다.\n")
                    continue
            except ValueError:
                print("잘못된 금액입니다. 숫자를 입력해주세요.\n")
                continue
            budget.add_expense(category, description, amount)
            print("지출이 추가되었습니다.\n")

        elif choice == "2":
            budget.list_expenses()

        elif choice == "3":
            budget.total_spent()

        elif choice == "4": # 충동소비 진정실 등록
            print("\n--- 충동소비 진정실 등록 ---")
            category = input("카테고리 (예: 전자기기, 옷, 취미용품 등): ")
            description = input("충동적으로 사고 싶은 물건/서비스 설명: ")
            try:
                amount = int(input("예상 금액(원): "))
                if amount <= 0:
                    print("금액은 0보다 커야 합니다.\n")
                    continue
            except ValueError:
                print("잘못된 금액입니다. 숫자를 입력해주세요.\n")
                continue
            
            impulse_controller.add_to_impulse_calm_room(category, description, amount)

        elif choice == "5": # 충동소비 진정실 목록 보기
            impulse_controller.view_impulse_calm_room()

        elif choice == "6": # 충동소비 실행실 입장
            print("\n--- 충동소비 실행실 입장 ---")
            if impulse_controller.view_points() == 0:
                print("포인트가 없습니다. 먼저 충동소비를 진정실에 등록해 포인트를 쌓아보세요!\n")
                continue
            
            try:
                points_to_spend = int(input("이번 뽑기에 사용할 포인트를 입력하세요 (얼마 이하의 상품을 뽑을까요?): "))
                if points_to_spend <= 0:
                    print("사용할 포인트는 0보다 커야 합니다.\n")
                    continue
            except ValueError:
                print("잘못된 포인트입니다. 숫자를 입력해주세요.\n")
                continue
            
            impulse_controller.execute_impulse_item(points_to_spend, budget)

        elif choice == "7": # 내 포인트 확인하기
            impulse_controller.view_points()

        elif choice == "8": # 종료
            print("가계부를 종료합니다.\n")
            break

        else:
            print("잘못된 선택입니다. 메뉴에 있는 번호를 입력해주세요.\n")


if __name__ == "__main__":
    main()
