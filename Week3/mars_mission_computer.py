import random
import datetime

class DummySensor:
    def __init__(self):
        # 환경 데이터를 저장할 딕셔너리 초기화
        self.env_values = {
            'inner_temp': 0.0,
            'outer_temp': 0.0,
            'humidity': 0,
            'light': 0,
            'co2': 0.0,
            'oxygen': 0.0
        }

    def set_env(self):
        '''범위에 맞는 랜덤 환경 데이터 생성'''
        self.env_values['inner_temp'] = round(random.uniform(18, 30), 1)
        self.env_values['outer_temp'] = round(random.uniform(0, 21), 1)
        self.env_values['humidity'] = random.randint(50, 60)
        self.env_values['light'] = random.randint(500, 715)
        self.env_values['co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['oxygen'] = round(random.uniform(4, 7), 1)
        print('--- 환경 데이터가 갱신되었습니다 ---')

    def get_env(self):
        '''현재 환경 데이터 반환 및 로그 저장 (보너스 구현)'''
        # 보너스: get_env() 실행 시 로그 파일 저장
        self._save_log()
        return self.env_values

    def _save_log(self):
        '''현재 시간을 포함하여 로그 파일에 저장하는 내부 메서드'''
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f'[{now}] Sensor Data: {self.env_values}\n'
        
        try:
            with open('sensor_history.log', 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f'로그 저장 중 오류 발생: {e}')

# --- 메인 실행부 ---
if __name__ == '__main__':
    # 4) 인스턴스 생성
    ds = DummySensor()

    # 5) set_env() -> get_env() 실행
    ds.set_env()
    current_data = ds.get_env()

    # 결과 출력
    print('현재 화성 기지 환경 상태:')
    for key, value in current_data.items():
        print(f'- {key}: {value}')
