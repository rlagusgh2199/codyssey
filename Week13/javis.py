import os
import csv
import speech_recognition as sr

class MarsVoiceAssistant:
    '''화성 기지의 음성 기록을 텍스트로 변환하고 검색하는 클래스입니다.'''

    def __init__(self):
        # STT 인식기 객체 초기화
        self.recognizer = sr.Recognizer()

    def transcribe_and_save(self, audio_dir):
        '''오디오 파일을 읽어 STT를 수행하고 CSV 파일로 저장합니다.'''
        print('=============================================')
        print('[SYSTEM] J.A.R.V.I.S STT 변환 프로토콜 가동')
        print('=============================================')

        # 지정된 디렉토리 내의 파일 목록을 불러옴
        for filename in os.listdir(audio_dir):
            if filename.endswith('.wav'):
                file_path = os.path.join(audio_dir, filename)
                csv_filename = filename.replace('.wav', '.csv')
                csv_path = os.path.join(audio_dir, csv_filename)

                print(f'\n분석 중: \'{filename}\'')

                try:
                    # 음성 파일 열기 및 읽기
                    with sr.AudioFile(file_path) as source:
                        audio_data = self.recognizer.record(source)

                        # 구글 Web Speech API를 활용한 텍스트 추출
                        text = self.recognizer.recognize_google(audio_data, language='ko-KR')

                        # 무료 STT API 특성상 단어별 시간 추출이 제한적이므로 시작 시간인 '00:00'을 부여
                        self._save_to_csv(csv_path, '00:00', text)
                        print(f'  -> STT 변환 성공! \'{csv_filename}\' 저장 완료.')

                except sr.UnknownValueError:
                    print(f'  -> 경고: \'{filename}\'의 음성을 명확히 인식할 수 없습니다.')
                except sr.RequestError as e:
                    print(f'  -> 시스템 오류: STT 서버 연결 실패 ({e})')
                except Exception as e:
                    print(f'  -> 알 수 없는 오류 발생: {e}')

    def _save_to_csv(self, csv_path, time_str, text):
        '''추출된 텍스트를 CSV 포맷으로 저장하는 내부 함수입니다.'''
        try:
            with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Time', 'Text'])
                writer.writerow([time_str, text])
        except Exception as e:
            print(f'CSV 저장 중 오류 발생: {e}')

    def search_keyword(self, audio_dir, keyword):
        '''[보너스 과제] 저장된 CSV 파일들 내에서 특정 키워드를 검색합니다.'''
        print('=============================================')
        print(f'[SYSTEM] \'{keyword}\' 키워드 데이터베이스 검색 중...')
        print('=============================================')

        found_flag = False

        for filename in os.listdir(audio_dir):
            if filename.endswith('.csv'):
                csv_path = os.path.join(audio_dir, filename)
                try:
                    with open(csv_path, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        next(reader)  # 헤더 행 건너뛰기

                        for row in reader:
                            if len(row) >= 2 and keyword in row[1]:
                                print(f'💡 발견 [{filename}] - 시간 {row[0]}: {row[1]}')
                                found_flag = True
                except Exception as e:
                    print(f'파일 읽기 오류 (\'{filename}\'): {e}')

        if not found_flag:
            print(f'경고: 데이터베이스 내에 \'{keyword}\'와 일치하는 기록이 없습니다.')

# --- 메인 실행부 ---
if __name__ == '__main__':
    # 제어 가능한 환경: 현재 파일 위치를 기준으로 디렉토리 설정
    base_dir = os.path.dirname(os.path.abspath(__file__))
    audio_directory = os.path.join(base_dir, 'audio_files')

    # 폴더가 없을 경우 자동 생성하여 FileNotFoundError 방어
    if not os.path.exists(audio_directory):
        os.makedirs(audio_directory)
        print(f'[SYSTEM] \'{audio_directory}\' 폴더를 생성했습니다. .wav 파일을 넣어주세요.')
    else:
        # 1. 객체 생성 및 STT 변환 수행
        javis = MarsVoiceAssistant()
        javis.transcribe_and_save(audio_directory)

        # 2. 보너스 과제: 키워드 검색 기능 수행
        print('\n')
        target_keyword = input('데이터베이스에서 검색할 키워드를 입력하세요: ')
        javis.search_keyword(audio_directory, target_keyword)