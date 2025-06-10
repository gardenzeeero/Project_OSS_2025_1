import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import re


class PuzzleCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("🧩 퍼즐 계산기")
        self.root.geometry("900x600")
        self.root.configure(bg='#2c3e50')

        self.expression = ""
        self.actual_expression = ""
        
        self.create_mappings()
        self.create_ui()
        
    def create_mappings(self):
        numbers = list(range(10))
        shuffled_numbers = numbers.copy()
        random.shuffle(shuffled_numbers)
        
        self.number_mapping = {}
        for i in range(10):
            self.number_mapping[str(numbers[i])] = str(shuffled_numbers[i])
        
        # 역 매핑 (실제 값 -> 표시 값)
        self.reverse_number_mapping = {v: k for k, v in self.number_mapping.items()}
        
        # 연산자 매핑
        operators = ['+', '-', '*', '/']
        shuffled_operators = operators.copy()
        random.shuffle(shuffled_operators)
        
        self.operator_mapping = {}
        for i in range(4):
            self.operator_mapping[operators[i]] = shuffled_operators[i]
        
        # 역 매핑
        self.reverse_operator_mapping = {v: k for k, v in self.operator_mapping.items()}
        
        # 사용자 추측 저장
        self.user_guesses = {
            'numbers': {str(i): '?' for i in range(10)},
            'operators': {op: '?' for op in operators}
        }

    def safe_eval(self, expression):
        try:
            # 0으로 시작하는 숫자들을 일반 10진수로 변환
            # 예: 05 -> 5, 07 -> 7
            fixed_expression = re.sub(r'\b0+(\d+)', r'\1', expression)
            fixed_expression = re.sub(r'\b0\b', '0', fixed_expression)
            return eval(fixed_expression)
        except:
            raise ValueError("계산 오류")

    def create_ui(self):
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # 상단: 제목과 설명
        title_frame = tk.Frame(main_frame, bg='#2c3e50')
        title_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(
            title_frame,
            text="🧩 퍼즐 계산기",
            font=("Arial", 20, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack()
        
        tk.Label(
            title_frame,
            text="숫자와 연산자가 섞여있어요! 계산 결과를 보고 실제 값을 추론해보세요!",
            font=("Arial", 12),
            bg='#2c3e50',
            fg='#bdc3c7'
        ).pack(pady=(5, 0))
        
        # 중간: 계산기와 추측 패널
        content_frame = tk.Frame(main_frame, bg='#2c3e50')
        content_frame.pack(fill="both", expand=True)
        
        # 왼쪽: 계산기
        calc_frame = tk.Frame(content_frame, bg='#2c3e50')
        calc_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        # 계산기 입력창
        self.entry = tk.Entry(
            calc_frame,
            font=("Arial", 18),
            justify="right",
            bg='#ecf0f1',
            fg='#2c3e50',
            insertbackground='#2c3e50',
            state='readonly'
        )
        self.entry.pack(fill="x", pady=(0, 20), ipady=10)
        
        # 계산기 버튼들
        buttons = [
            ['C', 'Hint', '=', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', 'New', 'Check']
        ]
        
        for row in buttons:
            button_frame = tk.Frame(calc_frame, bg='#2c3e50')
            button_frame.pack(fill="x", pady=2)
            
            for char in row:
                if char == '=':
                    bg_color = '#ff7675'
                    text_color = '#2c3e50'
                elif char in ['C', 'New', 'Check', 'Hint']:
                    bg_color = '#a29bfe'
                    text_color = '#2c3e50'
                elif char in ['+', '-', '*', '/']:
                    bg_color = '#74b9ff'
                    text_color = '#2c3e50'
                else:
                    bg_color = '#ecf0f1'
                    text_color = '#2c3e50'
                
                btn = tk.Button(
                    button_frame,
                    text=char,
                    font=("Arial", 16, "bold"),
                    bg=bg_color,
                    fg=text_color,
                    command=lambda ch=char: self.on_click(ch),
                    relief='flat',
                    width=4,
                    height=2
                )
                btn.pack(side="left", expand=True, fill="both", padx=1)
        
        # 오른쪽: 추측 패널
        guess_panel = tk.Frame(content_frame, bg='#2c3e50', width=400)
        guess_panel.pack(side="right", fill="y")
        guess_panel.pack_propagate(False)
        
        # 추측 패널 제목
        tk.Label(
            guess_panel,
            text="🤔 추측 패널",
            font=("Arial", 16, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack(pady=(0, 15))
        
        # 버튼 선택 섹션
        button_select_frame = tk.LabelFrame(
            guess_panel,
            text="1. 버튼 선택",
            font=("Arial", 12, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        button_select_frame.pack(fill="x", pady=(0, 15))
        
        # 버튼 선택을 위한 변수
        self.selected_button = tk.StringVar(value="0")
        
        # 숫자 버튼들 선택
        num_frame = tk.Frame(button_select_frame, bg='#2c3e50')
        num_frame.pack(pady=10)
        
        tk.Label(
            num_frame,
            text="숫자:",
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#bdc3c7'
        ).pack()
        
        num_buttons_frame = tk.Frame(num_frame, bg='#2c3e50')
        num_buttons_frame.pack(pady=5)
        
        for i in range(10):
            tk.Radiobutton(
                num_buttons_frame,
                text=str(i),
                variable=self.selected_button,
                value=str(i),
                bg='#2c3e50',
                fg='white',
                selectcolor='#34495e',
                font=("Arial", 10)
            ).pack(side="left", padx=2)
        
        # 연산자 버튼들 선택
        op_frame = tk.Frame(button_select_frame, bg='#2c3e50')
        op_frame.pack(pady=5)
        
        tk.Label(
            op_frame,
            text="연산자:",
            font=("Arial", 10),
            bg='#2c3e50',
            fg='#bdc3c7'
        ).pack()
        
        op_buttons_frame = tk.Frame(op_frame, bg='#2c3e50')
        op_buttons_frame.pack(pady=5)
        
        for op in ['+', '-', '*', '/']:
            tk.Radiobutton(
                op_buttons_frame,
                text=op,
                variable=self.selected_button,
                value=op,
                bg='#2c3e50',
                fg='white',
                selectcolor='#34495e',
                font=("Arial", 12)
            ).pack(side="left", padx=5)
        
        # 추측값 입력 섹션
        guess_input_frame = tk.LabelFrame(
            guess_panel,
            text="2. 실제 값 추측",
            font=("Arial", 12, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        guess_input_frame.pack(fill="x", pady=(0, 15))
        
        self.guess_entry = tk.Entry(
            guess_input_frame,
            font=("Arial", 14),
            justify="center",
            bg='#34495e',
            fg='white',
            insertbackground='white',
            width=10
        )
        self.guess_entry.pack(pady=10)
        
        # 추측 제출 버튼
        tk.Button(
            guess_input_frame,
            text="추측 제출",
            font=("Arial", 12, "bold"),
            bg='#55efc4',
            fg='#2c3e50',
            command=self.submit_guess,
            relief='flat'
        ).pack(pady=(0, 10))
        
        # 정답판 섹션
        answer_frame = tk.LabelFrame(
            guess_panel,
            text="🎯 정답판",
            font=("Arial", 12, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        answer_frame.pack(fill="both", expand=True)
        
        # 숫자 정답판
        numbers_frame = tk.Frame(answer_frame, bg='#2c3e50')
        numbers_frame.pack(fill="x", pady=5)
        
        tk.Label(
            numbers_frame,
            text="숫자 매핑:",
            font=("Arial", 10, "bold"),
            bg='#2c3e50',
            fg='#bdc3c7'
        ).pack()
        
        self.number_labels = {}
        num_grid_frame = tk.Frame(numbers_frame, bg='#2c3e50')
        num_grid_frame.pack(pady=5)
        
        for i in range(10):
            row = i // 5
            col = i % 5
            
            item_frame = tk.Frame(num_grid_frame, bg='#2c3e50')
            item_frame.grid(row=row, column=col, padx=5, pady=2)
            
            tk.Label(
                item_frame,
                text=f"{i}:",
                font=("Arial", 9),
                bg='#2c3e50',
                fg='#bdc3c7',
                width=2
            ).pack(side="left")
            
            self.number_labels[str(i)] = tk.Label(
                item_frame,
                text="?",
                font=("Arial", 9, "bold"),
                bg='#34495e',
                fg='#f39c12',
                width=2
            )
            self.number_labels[str(i)].pack(side="left")
        
        # 연산자 정답판
        operators_frame = tk.Frame(answer_frame, bg='#2c3e50')
        operators_frame.pack(fill="x", pady=10)
        
        tk.Label(
            operators_frame,
            text="연산자 매핑:",
            font=("Arial", 10, "bold"),
            bg='#2c3e50',
            fg='#bdc3c7'
        ).pack()
        
        self.operator_labels = {}
        op_grid_frame = tk.Frame(operators_frame, bg='#2c3e50')
        op_grid_frame.pack(pady=5)
        
        for i, op in enumerate(['+', '-', '*', '/']):
            item_frame = tk.Frame(op_grid_frame, bg='#2c3e50')
            item_frame.grid(row=0, column=i, padx=5, pady=2)
            
            tk.Label(
                item_frame,
                text=f"{op}:",
                font=("Arial", 9),
                bg='#2c3e50',
                fg='#bdc3c7',
                width=2
            ).pack(side="left")
            
            self.operator_labels[op] = tk.Label(
                item_frame,
                text="?",
                font=("Arial", 9, "bold"),
                bg='#34495e',
                fg='#f39c12',
                width=2
            )
            self.operator_labels[op].pack(side="left")
        
        # 점수 표시
        self.score_label = tk.Label(
            answer_frame,
            text="정답률: 0/14 (0%)",
            font=("Arial", 12, "bold"),
            bg='#2c3e50',
            fg='#2ecc71'
        )
        self.score_label.pack(pady=10)

    def submit_guess(self):
        """추측 제출 처리"""
        selected = self.selected_button.get()
        guess = self.guess_entry.get().strip()
        
        if not selected:
            messagebox.showwarning("경고", "버튼을 선택해주세요!")
            return
        
        if not guess:
            messagebox.showwarning("경고", "추측값을 입력해주세요!")
            return
        
        # 추측이 맞는지 확인
        if selected.isdigit():
            # 숫자 추측
            correct_value = self.number_mapping[selected]
            if guess == correct_value:
                self.user_guesses['numbers'][selected] = guess
                messagebox.showinfo("정답!", f"맞습니다! 버튼 {selected}은(는) 실제로 {guess}입니다! 🎉")
            else:
                messagebox.showinfo("틀렸어요", f"틀렸습니다. 버튼 {selected}은(는) {guess}이(가) 아닙니다. 😅")
        else:
            # 연산자 추측
            if guess in ['+', '-', '*', '/']:
                correct_value = self.operator_mapping[selected]
                if guess == correct_value:
                    self.user_guesses['operators'][selected] = guess
                    op_names = {'+': '더하기', '-': '빼기', '*': '곱하기', '/': '나누기'}
                    messagebox.showinfo("정답!", f"맞습니다! 버튼 {selected}은(는) 실제로 {guess}({op_names[guess]})입니다! 🎉")
                else:
                    messagebox.showinfo("틀렸어요", f"틀렸습니다. 버튼 {selected}은(는) {guess}이(가) 아닙니다. 😅")
            else:
                messagebox.showwarning("경고", "연산자는 +, -, *, / 중 하나를 입력해주세요!")
                return
        
        # 입력 필드 초기화
        self.guess_entry.delete(0, tk.END)
        self.selected_button.set("")
        
        self.update_display()

    def on_click(self, char):
        if char == 'C':
            self.expression = ""
            self.actual_expression = ""
        elif char == 'New':
            self.new_game()
        elif char == 'Check':
            self.check_all_answers()
        elif char == 'Hint':
            self.give_hint()
        elif char == '=':
            if self.actual_expression:
                try:
                    result = self.safe_eval(self.actual_expression)
                    self.expression += f" = {result}"
                    # 실제 계산식은 보여주지 않음
                    self.actual_expression = ""  # 초기화
                except:
                    self.expression += " = 에러"
                    self.actual_expression = ""
        elif char == '.':
            self.expression += char
            self.actual_expression += char
        elif char.isdigit():
            self.expression += char
            actual_digit = self.number_mapping[char]
            self.actual_expression += actual_digit
        elif char in ['+', '-', '*', '/']:
            self.expression += char
            actual_op = self.operator_mapping[char]
            self.actual_expression += actual_op
        
        self.update_entries()

    def update_entries(self):
        self.entry.config(state='normal')
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.expression)
        self.entry.config(state='readonly')

    def update_display(self):
        # 숫자 정답판 업데이트
        for num, guess in self.user_guesses['numbers'].items():
            color = '#2ecc71' if guess != '?' else '#f39c12'
            self.number_labels[num].config(text=guess, fg=color)
        
        # 연산자 정답판 업데이트
        for op, guess in self.user_guesses['operators'].items():
            color = '#2ecc71' if guess != '?' else '#f39c12'
            self.operator_labels[op].config(text=guess, fg=color)
        
        # 점수 업데이트
        total = 14  # 숫자 10개 + 연산자 4개
        correct = sum(1 for guess in self.user_guesses['numbers'].values() if guess != '?')
        correct += sum(1 for guess in self.user_guesses['operators'].values() if guess != '?')
        percentage = int((correct / total) * 100)
        
        self.score_label.config(text=f"정답률: {correct}/{total} ({percentage}%)")

    def give_hint(self):
        # 무작위로 하나의 힌트 제공
        unknown_numbers = [k for k, v in self.user_guesses['numbers'].items() if v == '?']
        unknown_operators = [k for k, v in self.user_guesses['operators'].items() if v == '?']
        
        all_unknown = unknown_numbers + unknown_operators
        
        if all_unknown:
            hint_item = random.choice(all_unknown)
            if hint_item in unknown_numbers:
                self.user_guesses['numbers'][hint_item] = self.number_mapping[hint_item]
                messagebox.showinfo("힌트", f"버튼 {hint_item}은(는) 실제로 {self.number_mapping[hint_item]}입니다!")
            else:
                self.user_guesses['operators'][hint_item] = self.operator_mapping[hint_item]
                op_names = {'+': '더하기', '-': '빼기', '*': '곱하기', '/': '나누기'}
                messagebox.showinfo("힌트", f"버튼 {hint_item}은(는) 실제로 {self.operator_mapping[hint_item]}({op_names[self.operator_mapping[hint_item]]})입니다!")
            
            self.update_display()
        else:
            messagebox.showinfo("완료", "모든 버튼의 정체를 알아냈습니다! 🎉")

    def check_all_answers(self):
        for num in range(10):
            self.user_guesses['numbers'][str(num)] = self.number_mapping[str(num)]
        
        for op in ['+', '-', '*', '/']:
            self.user_guesses['operators'][op] = self.operator_mapping[op]
        
        self.update_display()
        messagebox.showinfo("정답 공개", "모든 정답을 공개했습니다! 🎯")

    def new_game(self):
        self.create_mappings()
        self.expression = ""
        self.actual_expression = ""
        self.guess_entry.delete(0, tk.END)
        self.selected_button.set("")
        self.update_entries()
        self.update_display()
        messagebox.showinfo("새 게임", "새로운 퍼즐이 시작되었습니다! 🎮")


# 기존 Calculator 클래스는 호환성을 위해 남겨둠
Calculator = PuzzleCalculator



