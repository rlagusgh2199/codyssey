#문제8 불안정한 미션 컴퓨터…
import platform
import json
import os
import time

# 시스템 정보를 위해 외부 라이브러리 psutil 사용 (제약사항 예외 허용)
try:
    import psutil
except ImportError:
    print('psutil 라이브러리가 필요합니다. (pip install psutil)')

class MissionComputer:
    def __init__(self):
        self.env_values = {}
        # 설정 파일 로드 (보너스 과제)
        self.settings = self._load_settings()

    def _load_settings(self):
        '''setting.txt에서 출력할 항목 리스트를 가져옵니다.'''
        settings = []
        if os.path.exists('setting.txt'):
            try:
                with open('setting.txt', 'r', encoding='utf-8') as f:
                    settings = [line.strip() for line in f.readlines() if line.strip()]
            except Exception as e:
                print(f'설정 파일 로드 중 오류: {e}')
        return settings

    def _filter_output(self, data_dict):
        '''settings에 정의된 항목만 필터링합니다. (설정이 없으면 전체 출력)'''
        if not self.settings:
            return data_dict
        return {k: v for k, v in data_dict.items() if k in self.settings}

    def get_mission_computer_info(self):
        '''운영체제, CPU, 메모리 등 시스템 기본 정보를 출력합니다.'''
        info = {}
        try:
            info['operating_system'] = platform.system()
            info['os_version'] = platform.version()
            info['cpu_type'] = platform.processor()
            info['cpu_count'] = os.cpu_count()
            # 바이트 단위를 GB로 변환하여 저장
            total_mem = psutil.virtual_memory().total / (1024 ** 3)
            info['memory_size_gb'] = round(total_mem, 2)
            
            filtered_info = self._filter_output(info)
            print('\n[미션 컴퓨터 시스템 정보]')
            print(json.dumps(filtered_info, indent=4, ensure_ascii=False))
        except Exception as e:
            print(f'시스템 정보 수집 중 오류 발생: {e}')

    def get_mission_computer_load(self):
        '''실시간 CPU 및 메모리 부하 정보를 출력합니다.'''
        load = {}
        try:
            # cpu_percent는 호출 간격이 필요하므로 interval 설정
            load['cpu_usage_percent'] = psutil.cpu_percent(interval=0.1)
            load['memory_usage_percent'] = psutil.virtual_memory().percent
            
            filtered_load = self._filter_output(load)
            print('\n[미션 컴퓨터 실시간 부하 상태]')
            print(json.dumps(filtered_load, indent=4, ensure_ascii=False))
        except Exception as e:
            print(f'부하 정보 수집 중 오류 발생: {e}')

# --- 메인 실행부 ---
if __name__ == '__main__':
    # MissionComputer를 runComputer라는 이름으로 인스턴스화
    runComputer = MissionComputer()

    # 시스템 정보 및 부하 정보 호출
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()
