import os
import wave
import pyaudio
from datetime import datetime

class MarsVoiceRecorder:
    '''화성 기지의 일상 기록을 위해 시스템 마이크로 음성을 녹음하는 클래스입니다.'''

    def __init__(self, record_dir='records'):
        # 오디오 녹음 설정 (CD 음질 수준)
        self.chunk = 1024           # 한 번에 읽어올 데이터 단위
        self.format = pyaudio.paInt16 # 16비트 포맷
        self.channels = 1           # 모노(1채널) 마이크
        self.rate = 44100           # 샘플링 레이트 (44.1kHz)

        # 저장 디렉토리 설정 (기본값: records)
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.record_dir = os.path.join(base_dir, record_dir)

        # 폴더가 없으면 자동 생성
        if not os.path.exists(self.record_dir):
            os.makedirs(self.record_dir)
            print(f'[SYSTEM] \'{self.record_dir}\' 폴더를 생성했습니다.')

    def record_audio(self, record_seconds=5):
        '''마이크를 통해 지정된 시간(초)만큼 음성을 녹음하고 파일로 저장합니다.'''
        audio = pyaudio.PyAudio()

        print('=============================================')
        print('[SYSTEM] J.A.R.V.I.S 음성 기록 프로토콜 가동')
        print(f'-> 녹음을 시작합니다... ({record_seconds}초 동안 말씀하세요)')
        print('=============================================')

        try:
            # 오디오 스트림 열기
            stream = audio.open(format=self.format,
                                channels=self.channels,
                                rate=self.rate,
                                input=True,
                                frames_per_buffer=self.chunk)

            frames = []

            # 지정된 시간만큼 데이터 조각(chunk)들을 읽어와 리스트에 저장
            for _ in range(0, int(self.rate / self.chunk * record_seconds)):
                data = stream.read(self.chunk)
                frames.append(data)

            print('\n[SYSTEM] 녹음이 완료되었습니다.')

            # 스트림 닫기 및 리소스 반환
            stream.stop_stream()
            stream.close()

        except Exception as e:
            print(f'[오류] 마이크 접근 또는 녹음 중 문제가 발생했습니다: {e}')
            return
        finally:
            audio.terminate()

        # 녹음된 데이터를 파일로 저장하는 함수 호출
        self._save_to_wav(audio, frames)

    def _save_to_wav(self, audio, frames):
        '''녹음된 오디오 프레임 데이터를 WAV 파일로 저장하는 내부 함수입니다.'''
        # 현재 날짜와 시간을 지정된 포맷('년월일-시간분초')으로 추출
        now = datetime.now()
        filename = now.strftime('%Y%m%d-%H%M%S') + '.wav'
        file_path = os.path.join(self.record_dir, filename)

        try:
            # wave 모듈을 사용하여 파일 저장
            with wave.open(file_path, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(audio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(frames))

            print(f'-> 저장 완료: \'{file_path}\'')
        except Exception as e:
            print(f'[오류] 오디오 파일 저장 중 문제가 발생했습니다: {e}')

    def show_records_by_date(self, start_date_str, end_date_str):
        '''[보너스 과제] 특정 범위의 날짜에 녹음된 파일 목록을 보여줍니다.'''
        print('=============================================')
        print(f'[SYSTEM] 데이터베이스 검색: {start_date_str} ~ {end_date_str}')
        print('=============================================')

        try:
            # 문자열 날짜를 datetime 객체로 변환 (예: '20260601')
            start_date = datetime.strptime(start_date_str, '%Y%m%d')
            end_date = datetime.strptime(end_date_str, '%Y%m%d')

            found_count = 0

            for filename in os.listdir(self.record_dir):
                if filename.endswith('.wav'):
                    # 파일 이름에서 날짜 부분('YYYYMMDD')만 추출
                    file_date_str = filename.split('-')[0]
                    file_date = datetime.strptime(file_date_str, '%Y%m%d')

                    # 파일 날짜가 지정된 범위(시작일 <= 파일일 <= 종료일) 안에 있는지 검사
                    if start_date <= file_date <= end_date:
                        print(f'- 검색된 파일: {filename}')
                        found_count += 1

            if found_count == 0:
                print('경고: 지정된 기간 내에 일치하는 녹음 기록이 없습니다.')

        except ValueError:
            print('[오류] 날짜 형식이 잘못되었습니다. YYYYMMDD 형식으로 입력하세요 (예: 20260601).')
        except Exception as e:
            print(f'[오류] 디렉토리 검색 중 문제가 발생했습니다: {e}')


# --- 메인 실행부 ---
if __name__ == '__main__':
    # 객체 생성 (기본값으로 현재 폴더 하위에 'records' 폴더 사용)
    recorder = MarsVoiceRecorder()

    # 1. 시스템 마이크로 5초간 녹음 테스트
    # (원하는 시간으로 파라미터를 변경할 수 있습니다.)
    recorder.record_audio(record_seconds=5)

    # 2. 보너스 과제: 날짜 범위를 입력받아 파일 검색 테스트
    print('\n[SYSTEM] 특정 기간의 녹음 기록을 검색합니다.')
    start_input = input('시작 날짜를 입력하세요 (예: 20260601): ')
    end_input = input('종료 날짜를 입력하세요 (예: 20260630): ')

    recorder.show_records_by_date(start_input, end_input)