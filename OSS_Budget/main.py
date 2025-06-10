from budget import Budget


def main():
    budget = Budget()

    while True:
        print("==== 간단 가계부 ====")
        print("1. 지출 추가")
        print("2. 지출 목록 보기")
        print("3. 총 지출 보기")
        print("4. 반성 점수 요약")
        print("5. 종료")
        choice = input("선택 > ")

        if choice == "1":
            category = input("카테고리 (예: 식비, 교통 등): ")
            description = input("설명: ")
            try:
                amount = int(input("금액(원): "))
            except ValueError:
                print("잘못된 금액입니다.\n")
                continue
            
            print("반성 점수 (1-10, 1: 전혀 후회 안됨, 10: 매우 후회됨)")
            try:
                reflection_score = int(input("반성 점수: "))
                if reflection_score < 1 or reflection_score > 10:
                    print("반성 점수는 1~10 사이여야 합니다.\n")
                    continue
            except ValueError:
                print("잘못된 반성 점수입니다.\n")
                continue
                
            budget.add_expense(category, description, amount, reflection_score)

        elif choice == "2":
            budget.list_expenses()

        elif choice == "3":
            budget.total_spent()

        elif choice == "4":
            budget.reflection_summary()

        elif choice == "5":
            print("가계부를 종료합니다.")
            break

        else:
            print("잘못된 선택입니다.\n")


if __name__ == "__main__":
    main()
