#3주차 / [과정 1] 1번 과제(미션 컴퓨터를 복구하고 사고 원인을 파악해 보자)
def main():
    # 1. 설치 확인용 출력
    print('Hello Mars')

    # 2. 파일명 변수 할당 (대입문 앞뒤 공백)
    log_filename = 'mission_computer_main.log'

    # 3. 예외 처리를 포함하여 파일 읽고 출력하기
    try:
        with open(log_filename, 'r', encoding='utf-8') as log_file:
            log_content = log_file.read()
            print(log_content)
    except FileNotFoundError:
        print('Error: 로그 파일을 찾을 수 없습니다.')
    except Exception as error:
        # 부득이하게 내부에 '를 포함한 문자열을 포매팅해야 하므로 " " 사용
        print(f"Error: 파일을 읽는 중 알 수 없는 오류가 발생했습니다. ({error})")

if __name__ == '__main__':
    main()
