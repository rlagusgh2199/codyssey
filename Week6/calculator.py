#8주차 문제3 계산기의 제작
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QGridLayout, QPushButton, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_expression = ''  # 현재 입력된 수식 저장

    def init_ui(self):
        '''아이폰 계산기 스타일의 UI 구성'''
        # 메인 레이아웃 (수직)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 1) 출력창 (아이폰 계산기의 검은 상단 화면 스타일)
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

        # 2) 버튼 배치 (그리드 레이아웃)
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(10)

        # 버튼 라벨 정의 (아이폰 배치 참고)
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
            
            # 버튼 클릭 이벤트 연결
            button.clicked.connect(lambda checked, t=text: self.on_button_click(t))
            buttons_layout.addWidget(button, row, col, 1, col_span)

        main_layout.addLayout(buttons_layout)
        
        # 윈도우 설정
        self.setLayout(main_layout)
        self.setWindowTitle('Mars Calculator')
        self.setStyleSheet("background-color: 'black';")
        self.setFixedSize(320, 500)

    def on_button_click(self, label):
        '''버튼 클릭 이벤트 처리 및 사칙연산 로직 (보너스 포함)'''
        if label == 'C':
            self.current_expression = ''
            self.display.setText('0')
        elif label == '=':
            try:
                # 보너스: 사칙연산 계산 기능
                result = str(eval(self.current_expression))
                self.display.setText(result)
                self.current_expression = result
            except Exception:
                self.display.setText('Error')
                self.current_expression = ''
        else:
            # 숫자가 0일 때 새로운 숫자를 입력하면 0을 지움
            if self.current_expression == '' and label in '0123456789':
                self.current_expression = label
            else:
                self.current_expression += label
            self.display.setText(self.current_expression)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec())
