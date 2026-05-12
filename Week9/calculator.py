import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QGridLayout, QPushButton, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        # --- 계산기 상태 관리 변수 ---
        self.current_value = '0'       # 화면에 표시되는 현재 입력값
        self.stored_value = None       # 연산자를 누르기 전 저장된 값
        self.current_operator = None   # 현재 선택된 연산자
        self.is_new_input = True       # 새로운 숫자를 입력받을 상태인지 여부

        self.init_ui()

    def init_ui(self):
        '''UI 레이아웃 구성 (이전 주차와 동일)'''
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        self.display = QLineEdit('0')
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setFixedHeight(80)
        self.display.setFont(QFont('Arial', 30))
        self.display.setStyleSheet('''
            background-color: '#1C1C1C';
            color: 'white';
            border: none;
            padding-right: 15px;
        ''')
        main_layout.addWidget(self.display)

        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(10)

        buttons = [
            ('C', 0, 0, '#A5A5A5', 'black'), ('±', 0, 1, '#A5A5A5', 'black'), ('%', 0, 2, '#A5A5A5', 'black'), ('/', 0, 3, '#FF9F0A', 'white'),
            ('7', 1, 0, '#333333', 'white'), ('8', 1, 1, '#333333', 'white'), ('9', 1, 2, '#333333', 'white'), ('*', 1, 3, '#FF9F0A', 'white'),
            ('4', 2, 0, '#333333', 'white'), ('5', 2, 1, '#333333', 'white'), ('6', 2, 2, '#333333', 'white'), ('-', 2, 3, '#FF9F0A', 'white'),
            ('1', 3, 0, '#333333', 'white'), ('2', 3, 1, '#333333', 'white'), ('3', 3, 2, '#333333', 'white'), ('+', 3, 3, '#FF9F0A', 'white'),
            ('0', 4, 0, '#333333', 'white', 2), ('.', 4, 2, '#333333', 'white'), ('=', 4, 3, '#FF9F0A', 'white')
        ]

        for btn_info in buttons:
            if len(btn_info) == 5:
                text, row, col, bg_color, text_color = btn_info
                col_span = 1
            else:
                text, row, col, bg_color, text_color, col_span = btn_info

            button = QPushButton(text)
            button.setFixedSize(70 * col_span + (10 if col_span > 1 else 0), 70)
            button.setFont(QFont('Arial', 18, QFont.Weight.Bold))
            button.setStyleSheet(f'''
                background-color: {bg_color};
                color: {text_color};
                border-radius: 35px;
            ''')

            button.clicked.connect(lambda checked, t=text: self.on_button_click(t))
            buttons_layout.addWidget(button, row, col, 1, col_span)

        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)
        self.setWindowTitle('Mars Calculator')
        self.setStyleSheet("background-color: 'black';")
        self.setFixedSize(320, 500)

    # --- 이벤트 라우팅 ---
    def on_button_click(self, label):
        if label in '0123456789':
            self.num_press(label)
        elif label == '.':
            self.dot_press()
        elif label == 'C':
            self.reset()
        elif label == '±':
            self.negative_positive()
        elif label == '%':
            self.percent()
        elif label in ['+', '-', '*', '/']:
            self.op_press(label)
        elif label == '=':
            self.equal()

        self.update_display()

    # --- 코어 동작 메서드 ---
    def num_press(self, val):
        '''숫자 입력 누적'''
        if self.is_new_input:
            self.current_value = val
            self.is_new_input = False
        else:
            if self.current_value == '0':
                self.current_value = val
            else:
                self.current_value += val

    def dot_press(self):
        '''소수점 입력 (중복 방지)'''
        if self.is_new_input:
            self.current_value = '0.'
            self.is_new_input = False
        elif '.' not in self.current_value:
            self.current_value += '.'

    def reset(self):
        '''C 버튼: 초기화'''
        self.current_value = '0'
        self.stored_value = None
        self.current_operator = None
        self.is_new_input = True

    def negative_positive(self):
        '''± 버튼: 양수/음수 전환'''
        if self.current_value in ['0', 'Error']:
            return
        if self.current_value.startswith('-'):
            self.current_value = self.current_value[1:]
        else:
            self.current_value = '-' + self.current_value

    def percent(self):
        '''% 버튼: 100으로 나누기'''
        try:
            val = float(self.current_value) / 100
            self.current_value = self.format_result(val)
            self.is_new_input = True
        except Exception:
            self.current_value = 'Error'

    def op_press(self, op):
        '''사칙연산 버튼 입력 시 상태 저장'''
        if not self.is_new_input and self.stored_value is not None:
            self.equal()  # 연속해서 연산자를 누를 경우 이전 값 계산

        try:
            self.stored_value = float(self.current_value)
            self.current_operator = op
            self.is_new_input = True
        except Exception:
            self.current_value = 'Error'

    # --- 사칙 연산 핵심 로직 ---
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError('0으로 나눌 수 없습니다.')
        return a / b

    def equal(self):
        '''= 버튼: 연산 수행 및 예외 처리'''
        if self.current_operator is None or self.stored_value is None:
            return

        try:
            a = self.stored_value
            b = float(self.current_value)
            result = 0

            if self.current_operator == '+':
                result = self.add(a, b)
            elif self.current_operator == '-':
                result = self.subtract(a, b)
            elif self.current_operator == '*':
                result = self.multiply(a, b)
            elif self.current_operator == '/':
                result = self.divide(a, b)

            # 범위 초과 예외 처리 (오버플로우 방지)
            if result > 1e100 or result < -1e100:
                raise OverflowError('범위 초과')

            self.current_value = self.format_result(result)

        except ZeroDivisionError:
            self.current_value = 'Error: Div by 0'
        except OverflowError:
            self.current_value = 'Error: Overflow'
        except Exception:
            self.current_value = 'Error'

        self.stored_value = None
        self.current_operator = None
        self.is_new_input = True

    # --- 보너스 과제 처리 ---
    def format_result(self, val):
        '''보너스: 소수점 6자리 이하 반올림 처리'''
        val = round(val, 6)
        # 소수점이 없는 정수형태라면 정수로 변환하여 '.0' 제거
        if val.is_integer():
            return str(int(val))
        return str(val)

    def update_display(self):
        '''보너스: 텍스트 길이에 따른 폰트 크기 동적 조절'''
        length = len(self.current_value)
        if length < 10:
            self.display.setFont(QFont('Arial', 30))
        elif length < 14:
            self.display.setFont(QFont('Arial', 22))
        else:
            self.display.setFont(QFont('Arial', 16))

        self.display.setText(self.current_value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec())