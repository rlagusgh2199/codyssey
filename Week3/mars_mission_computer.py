#5주차 / 문제6 미션 컴퓨터 리턴즈
import random
import datetime

class DummySensor:
    def __init__(self):
        # 멤버 변수 env_values 초기화
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }

    def set_env(self):
        '''범위 내 랜덤 값을 생성하여 env_values를 갱신합니다.'''
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        '''현재 환경 데이터를 반환하고 로그 파일에 저장합니다.'''
        # 보너스 과제: 파일에 로그 기록
        self._write_log()
        return self.env_values

    def _write_log(self):
        '''데이터를 날짜/시간과 함께 mission_log.txt에 기록하는 내부 메서드'''
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_msg = f'[{now}] '
        
        # 딕셔너리의 모든 항목을 문자열로 변환하여 결합
        items = []
        for key, value in self.env_values.items():
            items.append(f'{key}: {value}')
        
        log_msg += ', '.join(items) + '\n'

        try:
            with open('mission_log.txt', 'a', encoding='utf-8') as f:
                f.write(log_msg)
        except Exception as e:
            print(f'로그 저장 중 오류 발생: {e}')

# 4) DummySensor 인스턴스 ds 생성
ds = DummySensor()

# 5) set_env()와 get_env() 차례로 호출하여 값 확인
ds.set_env()
current_env = ds.get_env()

# 결과 출력
print('--- 화성 기지 현재 환경 데이터 ---')
for sensor, val in current_env.items():
    print(f'{sensor}: {val}')
print('----------------------------------')
print('로그가 mission_log.txt에 저장되었습니다.')
