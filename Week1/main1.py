def main():
    print('Hello Mars')

    log_filename = 'mission_computer_main.log'
    
    # 분석의 타겟이 되는 핵심 키워드 설정
    target_keywords = ['explosion', 'unstable', 'ERROR', 'WARNING']
    anomaly_count = 0

    try:
        # 파일을 엽니다. (with문이 끝나면 자동으로 닫힘)
        with open(log_filename, 'r', encoding='utf-8') as log_file:
            
            # 첫 번째 줄(헤더: timestamp,event,message)은 분석 대상이 아니므로 한 줄 읽어서 넘깁니다.
            header = log_file.readline()
            
            print('--- 이상 징후(Anomaly) 탐지 결과 ---')
            
            # 대용량 처리를 위한 핵심: 파일을 한 줄씩만 메모리에 올려서 처리 (Streaming)
            for line in log_file:
                # 읽어온 한 줄에 타겟 키워드가 포함되어 있는지 검사
                for keyword in target_keywords:
                    if keyword in line:
                        # 줄바꿈 기호(\n)를 제거(strip)하고 깔끔하게 출력
                        print(line.strip())
                        anomaly_count += 1
                        break  # 한 줄에 여러 키워드가 있어도 중복 카운트 방지
            
            print(f'\n분석 완료: 총 {anomaly_count}개의 이상 징후가 발견되었습니다.')

    except FileNotFoundError:
        print('Error: 로그 파일을 찾을 수 없습니다.')
    except Exception as error:
        print(f'Error: 파일을 읽는 중 알 수 없는 오류가 발생했습니다. ({error})')

if __name__ == '__main__':
    main()