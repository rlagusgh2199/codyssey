import os
import zipfile
import itertools
import time
import string
import multiprocessing

def save_password(password):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    txt_path = os.path.join(base_dir, 'password.txt')
    try:
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(password)
        print('\n--- password.txt 파일에 비밀번호 저장 완료 ---')
    except Exception:
        pass

def _worker_task(pwd_chunk, zip_path):
    '''할당받은 비밀번호 뭉치를 극한의 속도로 메모리에서 검증'''
    count = 0
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            # [최적화 1] 매번 파일 이름을 검색하지 않고, 파일 객체(ZipInfo)를 미리 가져옴
            target_info = zf.filelist[0]

            for pwd_str in pwd_chunk:
                count += 1
                # [최적화 2] 문자열을 바이트(bytes)로 변환하는 작업을 미리 처리
                pwd_bytes = pwd_str.encode('utf-8')
                try:
                    # [최적화 3] extractall() 대신 단일 파일 메모리 읽기(read) 사용
                    zf.read(target_info, pwd=pwd_bytes)
                    return pwd_str, count
                except Exception:
                    pass
    except Exception:
        pass
    return None, count

def password_generator():
    '''40초 컷을 위한 스마트 경우의 수 생성기'''
    alphas = string.ascii_lowercase
    digits = string.digits

    # 전략 1: "숫자로만 된 6자리" (100만 개) - 멀티프로세싱 시 10~40초 내외 컷!
    for attempt in itertools.product(digits, repeat=6):
        yield ''.join(attempt)

    # 전략 2: 첫 글자가 알파벳인 경우 (a~z 순차 탐색)
    # 정답이 a, b, c 등 앞쪽에 있다면 몇 분 안에 찾음
    all_chars = alphas + digits
    for start_char in alphas:
        for attempt in itertools.product(all_chars, repeat=5):
            yield start_char + ''.join(attempt)

    # 전략 3: 나머지 모든 경우 (숫자로 시작하고 문자가 섞인 경우)
    for start_char in digits:
        for attempt in itertools.product(all_chars, repeat=5):
            pwd = start_char + ''.join(attempt)
            # 전략 1에서 이미 한 순수 숫자는 제외
            if not pwd.isdigit():
                yield pwd

def unlock_zip_extreme():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(base_dir, 'emergency_storage_key.zip')

    if not os.path.exists(zip_path):
        print(f'\n❌ 오류: {zip_path} 파일이 없습니다.')
        return

    start_time = time.time()
    print('\n[SYSTEM] 극한의 멀티프로세싱 엔진 가동 (40초 컷 도전...)')
    print('1단계: 순수 숫자 6자리(100만 개) 초고속 병렬 탐색 중...')

    gen = password_generator()
    chunk_size = 50000  # 한 프로세스당 5만 개씩 할당하여 병목 최소화

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    total_count = 0

    while True:
        chunks = []
        for _ in range(multiprocessing.cpu_count() * 4):
            chunk = list(itertools.islice(gen, chunk_size))
            if not chunk:
                break
            chunks.append((chunk, zip_path))

        if not chunks:
            break

        # 병렬 처리 시작
        results = pool.starmap(_worker_task, chunks)

        for res_pwd, count in results:
            total_count += count
            if res_pwd:
                elapsed_time = time.time() - start_time
                print('\n========================================')
                print('[SYSTEM] 해킹 성공! 문이 열립니다.')
                print(f'🔑 찾아낸 비밀번호: {res_pwd}')
                print(f'⏱ 진행 소요 시간: {elapsed_time:.2f}초')
                print(f'🔄 탐색한 총 횟수: {total_count}회')
                print('========================================')

                try:
                    with zipfile.ZipFile(zip_path, 'r') as zf:
                        zf.extractall(path=base_dir, pwd=res_pwd.encode('utf-8'))
                except Exception:
                    pass

                save_password(res_pwd)
                pool.terminate()
                return res_pwd

    print('\n[SYSTEM] 비밀번호를 찾지 못했습니다.')
    pool.close()

if __name__ == '__main__':
    unlock_zip_extreme()