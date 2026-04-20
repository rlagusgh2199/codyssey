#6주차 / 문제7 살아난 미션 컴퓨터
import random
import time
import datetime
import json

class DummySensor:
    '''환경 데이터를 랜덤으로 생성하는 더미 센서 클래스'''
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }

    def set_env(self):
        '''범위 내 랜덤 값을 생성하여 env_values를 갱신'''
        self.env_values['mars_base_internal_temperature'] = round(random.uniform(18, 30), 2)
        self.env_values['mars_base_external_temperature'] = round(random.uniform(0, 21), 2)
        self.env_values['mars_base_internal_humidity'] = round(random.uniform(50, 60), 2)
        self.env_values['mars_base_external_illuminance'] = round(random.uniform(500, 715), 2)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        '''현재 환경 데이터를 반환'''
        return self.env_values


class MissionComputer:
    '''센서 데이터를 수집하고 관리하는 미션 컴퓨터 클래스'''
    def __init__(self):
        self.env_values = {}
        self.ds = DummySensor()  # DummySensor 인스턴스화
        self.history = []        # 평균 계산을 위한 데이터 저장소
        self.last_avg_time = time.time()

    def get_sensor_data(self):
        '''5초마다 센서 데이터를 수집, 출력하고 5분마다 평균을 계산'''
        print('--- 미션 컴퓨터 가동 시작 (중단하려면 Ctrl+C를 누르세요) ---')
        
        try:
            while True:
                # 1) 센서 값 가져와서 env_values에 담기
                self.ds.set_env()
                self.env_values = self.ds.get_env()
                self.history.append(self.env_values.copy())

                # 2) JSON 형태로 화면에 출력
                print(f'\n[실시간 환경 데이터 - {datetime.datetime.now().strftime("%H:%M:%S")}]')
                print(json.dumps(self.env_values, indent=4))

                # 보너스: 5분(300초)마다 평균값 출력
                current_time = time.time()
                if current_time - self.last_avg_time >= 300:
                    self._display_average()
                    self.last_avg_time = current_time
                    self.history = []  # 리스트 초기화

                # 3) 5초 대기
                time.sleep(5)
                
        except KeyboardInterrupt:
            # 보너스: 특정 키(Ctrl+C) 입력 시 중단
            print('\nSystem stopped....')

    def _display_average(self):
        '''누적된 데이터의 평균값을 계산하여 출력'''
        if not self.history:
            return

        avg_values = {}
        keys = self.history[0].keys()
        
        for key in keys:
            total = sum(data[key] for data in self.history)
            avg_values[key] = round(total / len(self.history), 3)

        print('\n' + '='*40)
        print('[최근 5분간 환경 데이터 평균값]')
        print(json.dumps(avg_values, indent=4))
        print('='*40)


# 메인 실행부
if __name__ == '__main__':
    # MissionComputer를 RunComputer라는 이름으로 인스턴스화
    RunComputer = MissionComputer()
    
    # 지속적으로 환경 데이터 출력 시작
    RunComputer.get_sensor_data()
