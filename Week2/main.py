def main():
    # 파일명 변수 할당 (대입문 앞뒤 공백, 작은따옴표 준수)
    input_csv = 'Mars_Base_Inventory_List.csv'
    output_csv = 'Mars_Base_Inventory_danger.csv'
    output_bin = 'Mars_Base_Inventory_List.bin'

    inventory_list = []

    # 1 & 2. CSV 파일을 읽어서 리스트(List) 객체로 변환 및 출력
    try:
        with open(input_csv, 'r', encoding='utf-8') as file:
            for line in file:
                # 줄바꿈 제거 후 콤마를 기준으로 리스트로 쪼갬
                row = line.strip().split(',')
                inventory_list.append(row)
                
        print('--- 1. 전체 인벤토리 목록 (리스트 변환) ---')
        for item in inventory_list:
            print(item)
            
    except FileNotFoundError:
        print('Error: 입력 CSV 파일을 찾을 수 없습니다.')
        return
    except Exception as error:
        print(f'Error: 파일을 읽는 중 오류가 발생했습니다. ({error})')
        return

    # 3. 배열 내용을 인화성이 높은 순(내림차순)으로 정렬
    header = inventory_list[0]
    data = inventory_list[1:]
    
    # 인화성 지수(5번째 항목, 인덱스 4)를 실수형(float)으로 변환하여 정렬
    try:
        data.sort(key=lambda x: float(x[4]), reverse=True)
        sorted_inventory = [header] + data
    except Exception as error:
        print(f'Error: 데이터 정렬 중 오류가 발생했습니다. ({error})')
        return

    # 4. 인화성 지수가 0.7 이상되는 목록을 뽑아서 별도 출력
    danger_list = [header]
    print('\n--- 2. 인화성 지수 0.7 이상 위험 물질 목록 ---')
    for row in data:
        if float(row[4]) >= 0.7:
            danger_list.append(row)
            print(row)

    # 5. 인화성 지수 0.7 이상 목록을 새로운 CSV 포맷으로 저장
    try:
        with open(output_csv, 'w', encoding='utf-8') as file:
            for row in danger_list:
                # 리스트를 다시 콤마(,)로 연결하여 문자열로 저장
                file.write(','.join(row) + '\n')
        print(f'\n[시스템 알림] {output_csv} 저장 완료.')
    except Exception as error:
        print(f'Error: CSV 파일 저장 중 오류가 발생했습니다. ({error})')

    # [보너스 1] 정렬된 배열의 내용을 이진 파일(Binary) 형태로 저장
    try:
        # 'wb' (Write Binary) 모드로 열기
        with open(output_bin, 'wb') as file:
            for row in sorted_inventory:
                line_str = ','.join(row) + '\n'
                # 문자열을 바이트(bytes) 객체로 인코딩하여 저장
                file.write(line_str.encode('utf-8'))
        print(f'[시스템 알림] {output_bin} 저장 완료.')
    except Exception as error:
        print(f'Error: 이진 파일 저장 중 오류가 발생했습니다. ({error})')

    # [보너스 2] 저장된 이진 파일을 다시 읽어 들여서 화면에 출력
    try:
        # 'rb' (Read Binary) 모드로 열기
        with open(output_bin, 'rb') as file:
            # 바이트 객체를 읽어와서 문자열로 디코딩(decode)
            binary_data = file.read().decode('utf-8')
            print('\n--- 3. 이진 파일 읽기 결과 ---')
            print(binary_data.strip())
    except Exception as error:
        print(f'Error: 이진 파일을 읽는 중 오류가 발생했습니다. ({error})')

if __name__ == '__main__':
    main()