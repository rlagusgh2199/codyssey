import os

def caesar_cipher_decode(target_text):
    '''카이사르 암호를 해독하고 결과를 반환 및 저장합니다.'''

    # [보너스 과제] 화성 생존 시나리오 기반 텍스트 사전 (휴리스틱 탐색용)
    dictionary = ['coffee', 'water', 'oxygen', 'mars', 'base', 'earth', 'survival', 'emergency', 'door']

    print('=============================================')
    print('미션 컴퓨터: 카이사르 암호 해독 프로토콜 가동')
    print('=============================================')

    # 해독된 텍스트들을 저장할 리스트 (인덱스 0은 비워둠)
    decoded_results = ['']

    # 1. 1부터 25까지 자리수(Shift) 이동하며 모든 경우의 수 출력
    for shift in range(1, 26):
        decoded_text = ''

        for char in target_text:
            if char.isalpha():
                # 대문자/소문자 구분하여 기준점(ASCII 코드) 설정
                base = ord('a') if char.islower() else ord('A')

                # CS 포인트: 모듈러(%) 연산을 이용한 알파벳 순환(Wrap-around)
                shifted_char = chr((ord(char) - base + shift) % 26 + base)
                decoded_text += shifted_char
            else:
                # 알파벳이 아닌 문자(공백, 특수문자 등)는 그대로 유지
                decoded_text += char

        decoded_results.append(decoded_text)
        print(f'[Shift {shift:2d}] {decoded_text}')

        # 2. [보너스 과제] 사전에 있는 단어가 포함되어 있는지 실시간 검사
        for word in dictionary:
            if word in decoded_text.lower():
                print('\n[SYSTEM] 💡 의미 있는 단어 발견! 자동 해독 성공.')
                print(f'- 매칭된 키워드: \'{word}\'')
                print(f'- 정답 Shift: {shift}')
                print(f'- 최종 해독문: {decoded_text}')
                _save_result(decoded_text)
                return  # 해독 성공 시 즉시 함수 종료

    # 3. 보너스 로직에서 단어를 찾지 못했을 경우 (수동 입력 대기)
    _manual_selection(decoded_results)

def _manual_selection(decoded_results):
    '''사용자가 눈으로 확인하고 직접 Shift 번호를 입력하는 내부 함수'''
    print('\n[SYSTEM] 사전에 등록된 단어를 찾지 못했습니다. 수동 분석 모드로 전환합니다.')
    while True:
        try:
            choice = int(input('가장 의미 있는 문장의 Shift 번호(1~25)를 입력하세요: '))
            if 1 <= choice <= 25:
                selected_text = decoded_results[choice]
                print(f'\n선택된 문장: {selected_text}')
                _save_result(selected_text)
                break
            else:
                print('경고: 1에서 25 사이의 숫자를 입력해야 합니다.')
        except ValueError:
            print('경고: 숫자로 입력해주세요.')

def _save_result(text):
    '''해독된 텍스트를 result.txt 파일로 저장하는 내부 함수'''
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'result.txt')

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print('--- result.txt 파일에 해독문 저장 완료 ---')
    except Exception as e:
        print(f'파일 저장 중 예기치 못한 오류 발생: {e}')

if __name__ == '__main__':
    # 제어 가능한 환경: 현재 파일의 절대 경로를 기준으로 파일 탐색
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pwd_path = os.path.join(base_dir, 'password.txt')

    # 파일 읽기 및 예외 처리
    try:
        with open(pwd_path, 'r', encoding='utf-8') as f:
            encrypted_text = f.read().strip()

        if encrypted_text:
            caesar_cipher_decode(encrypted_text)
        else:
            print(f'경고: {pwd_path} 파일이 비어있습니다.')

    except FileNotFoundError:
        print(f'오류: {pwd_path} 파일을 찾을 수 없습니다.')
        print('이전 과제에서 생성된 password.txt 파일이 같은 폴더에 있는지 확인하세요.')
    except Exception as e:
        print(f'파일 처리 중 오류 발생: {e}')