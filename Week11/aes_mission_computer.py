import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class AES256Cipher:
    def __init__(self, key_b64=None):
        # [수정된 부분] 문자열(Base64) 형태의 키가 들어오면 그걸 사용하고, 없으면 새로 생성합니다.
        if key_b64:
            self.key = base64.b64decode(key_b64)
        else:
            self.key = os.urandom(32)

    def get_key_base64(self):
        '''생성된 키를 텍스트로 보관하기 위해 Base64로 인코딩하여 반환'''
        return base64.b64encode(self.key).decode('utf-8')

    def encrypt(self, plaintext):
        '''평문을 AES-256 (GCM 모드)로 암호화합니다.'''
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        plaintext_bytes = plaintext.encode('utf-8')
        ciphertext = encryptor.update(plaintext_bytes) + encryptor.finalize()

        encrypted_data = iv + encryptor.tag + ciphertext
        return base64.b64encode(encrypted_data).decode('utf-8')

    def decrypt(self, encrypted_text_base64):
        '''AES-256 암호문을 다시 평문으로 복호화합니다.'''
        encrypted_data = base64.b64decode(encrypted_text_base64)
        iv = encrypted_data[:16]
        tag = encrypted_data[16:32]
        ciphertext = encrypted_data[32:]

        cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()

        plaintext_bytes = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext_bytes.decode('utf-8')


# --- 메인 실행부 (화성 생존 시나리오 적용) ---
if __name__ == '__main__':
    # 제어 가능한 환경 (절대 경로 설정)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    key_path = os.path.join(base_dir, 'aes_master_key.txt')
    pwd_path = os.path.join(base_dir, 'aes_password.txt')
    result_path = os.path.join(base_dir, 'aes_result.txt')

    print("==================================================")
    print("[SYSTEM] 1단계: 출제자 모드 (데이터 암호화 및 보관)")
    print("==================================================\n")

    target_message = "I love Mars"

    # 1. 암호화 객체 생성 및 마스터 키 추출
    creator_aes = AES256Cipher()
    secret_key_b64 = creator_aes.get_key_base64()

    # 2. "I love Mars" 암호화
    encrypted_msg = creator_aes.encrypt(target_message)

    # 3. 키와 암호문을 각각 다른 파일에 저장
    with open(key_path, 'w', encoding='utf-8') as f:
        f.write(secret_key_b64)
    with open(pwd_path, 'w', encoding='utf-8') as f:
        f.write(encrypted_msg)

    print(f"📄 원본 데이터: {target_message}")
    print(f"🔒 마스터 키 저장 완료 -> {key_path}")
    print(f"🔒 암호문 저장 완료 -> {pwd_path}\n")


    print("==================================================")
    print("[SYSTEM] 2단계: 해결자 모드 (파일 로드 및 복호화)")
    print("==================================================\n")

    # 1. 파일에서 키와 암호문 읽어오기
    try:
        with open(key_path, 'r', encoding='utf-8') as f:
            loaded_key = f.read().strip()
        with open(pwd_path, 'r', encoding='utf-8') as f:
            loaded_ciphertext = f.read().strip()

        print("[SYSTEM] 마스터 키와 암호문을 성공적으로 로드했습니다.")

        # 2. 로드한 키를 넣어서 복호화 전용 객체 생성
        solver_aes = AES256Cipher(key_b64=loaded_key)

        # 3. 복호화 진행
        decrypted_msg = solver_aes.decrypt(loaded_ciphertext)

        # 4. 정답 파일에 저장
        with open(result_path, 'w', encoding='utf-8') as f:
            f.write(decrypted_msg)

        print(f"🔓 복호화 성공! 정답: {decrypted_msg}")
        print(f"💾 해독 결과 저장 완료 -> {result_path}")

    except FileNotFoundError:
        print("❌ 오류: 필요한 파일(키 또는 암호문)을 찾을 수 없습니다.")
    except Exception as e:
        print(f"❌ 복호화 실패: 키가 잘못되었거나 데이터가 변조되었습니다. ({e})")