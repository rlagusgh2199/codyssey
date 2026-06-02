import os
import csv
import mysql.connector
from mysql.connector import Error

class MySQLHelper:
    '''[보너스 과제] MySQL 데이터베이스 연결 및 쿼리 실행을 전담하는 헬퍼 클래스입니다.'''

    def __init__(self, host, user, password, database):
        self.connection = None
        try:
            # MySQL 데이터베이스 연결 시도
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.connection.is_connected():
                print('[SYSTEM] MySQL 데이터베이스에 성공적으로 연결되었습니다.')
        except Error as e:
            print(f'[오류] 데이터베이스 연결 실패: {e}')

    def execute_query(self, query, data=None):
        '''단일 쿼리(CREATE, INSERT 등)를 실행하고 커밋합니다.'''
        if not self.connection or not self.connection.is_connected():
            print('[오류] 데이터베이스에 연결되어 있지 않습니다.')
            return False

        cursor = self.connection.cursor()
        try:
            # 데이터(튜플)가 전달된 경우 매개변수화된 쿼리 실행 (SQL 인젝션 방지)
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)

            self.connection.commit()
            return True
        except Error as e:
            print(f'[오류] 쿼리 실행 실패: {e}')
            self.connection.rollback()
            return False
        finally:
            cursor.close()

    def close(self):
        '''데이터베이스 연결을 안전하게 종료합니다.'''
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print('[SYSTEM] MySQL 연결이 안전하게 종료되었습니다.')


# --- 메인 파이프라인 실행부 ---
def main():
    print('=============================================')
    print('미션 컴퓨터: 화성 기상 데이터 동기화 프로토콜')
    print('=============================================')

    # [수정 필요] 본인의 MySQL 환경에 맞게 접속 정보를 변경하세요.
    db_host = '127.0.0.1'
    db_user = 'root'
    db_pass = '1234'       # 설정하신 MySQL 비밀번호
    db_name = 'mars_db'    # Workbench에서 미리 만들어둔 스키마 이름

    # 1. 헬퍼 객체 생성 (데이터베이스 연결)
    db_helper = MySQLHelper(db_host, db_user, db_pass, db_name)

    # 2. 날씨 테이블(mars_weather) 생성 쿼리
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS mars_weather (
            weather_id INT AUTO_INCREMENT PRIMARY KEY,
            mars_date DATETIME NOT NULL,
            temp INT,
            storm INT
        )
    '''
    print('\n[SYSTEM] 테이블 스키마 검증 및 생성 중...')
    db_helper.execute_query(create_table_query)
    print('-> mars_weather 테이블 준비 완료.')

    # 3. CSV 파일 읽기 및 INSERT 반복 실행
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(base_dir, 'mars_weathers_data.csv')

    insert_query = '''
        INSERT INTO mars_weather (mars_date, temp, storm)
        VALUES (%s, %s, %s)
    '''

    print(f'\n[SYSTEM] \'{csv_file_path}\' 파일에서 데이터를 읽어옵니다...')

    try:
        with open(csv_file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # 첫 번째 행(헤더)은 데이터가 아니므로 건너뜁니다.

            insert_count = 0
            for row in reader:
                # row 데이터 예시: ['2026-06-01 12:00:00', '-60', '0']
                if len(row) >= 3:
                    mars_date = row[0]
                    temp = int(row[1])
                    storm = int(row[2])

                    # 반복적으로 INSERT 쿼리 실행
                    success = db_helper.execute_query(insert_query, (mars_date, temp, storm))
                    if success:
                        insert_count += 1

            print(f'-> 총 {insert_count}개의 날씨 데이터가 성공적으로 DB에 삽입되었습니다.')

    except FileNotFoundError:
        print(f'[오류] \'{csv_file_path}\' 파일을 찾을 수 없습니다. 같은 폴더에 파일이 있는지 확인하세요.')
    except ValueError as e:
        print(f'[오류] 데이터 변환 중 문제가 발생했습니다 (데이터 타입 불일치): {e}')
    except Exception as e:
        print(f'[오류] 예기치 못한 오류 발생: {e}')
    finally:
        # 4. 모든 작업이 끝나면 DB 연결 종료
        print('\n')
        db_helper.close()

if __name__ == '__main__':
    main()