#pip install cryptography
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class AES256Cipher:
    def __init__(self, key=None):
        # AES-256은 32바이트(256비트) 키를 사용합니다.
        # 키가 주어지지 않으면 안전한 난수로 새로 생성합니다.
        self.key = key if key else os.urandom(32)

    def get_key_base64(self):
        '''생성된 키를 텍스트로 보관하기 위해 Base64로 인코딩하여 반환'''
        return base64.b64encode(self.key).decode('utf-8')

    def encrypt(self, plaintext):
        '''평문을 AES-256 (GCM 모드)로 암호화합니다.'''
        # IV (Initialization Vector): 암호화할 때마다 달라지는 16바이트 소금(Salt) 역할
        iv = os.urandom(16)

        # AES-256 알고리즘과 GCM 모드(데이터 변조 방지 기능 포함) 설정
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # 문자열을 바이트로 변환 후 암호화
        plaintext_bytes = plaintext.encode('utf-8')
        ciphertext = encryptor.update(plaintext_bytes) + encryptor.finalize()

        # 복호화에 필요한 IV와 인증 태그(Tag)를 암호문과 함께 묶어서 반환 (Base64 인코딩)
        # 구조: IV(16바이트) + Tag(16바이트) + 암호문
        encrypted_data = iv + encryptor.tag + ciphertext
        return base64.b64encode(encrypted_data).decode('utf-8')

    def decrypt(self, encrypted_text_base64):
        '''AES-256 암호문을 다시 평문으로 복호화합니다.'''
        # Base64 문자열을 다시 바이트로 디코딩
        encrypted_data = base64.b64decode(encrypted_text_base64)

        # 묶여있던 IV, Tag, 실제 암호문을 분리
        iv = encrypted_data[:16]
        tag = encrypted_data[16:32]
        ciphertext = encrypted_data[32:]

        # 복호화 객체 생성
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv, tag), backend=default_backend())
        decryptor = cipher.decryptor()

        # 복호화 수행 및 문자열로 변환
        plaintext_bytes = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext_bytes.decode('utf-8')


# --- 메인 실행부 (화성 생존 시나리오 적용) ---
if __name__ == '__main__':
    print("==================================================")
    print("[SYSTEM] 차세대 미션 컴퓨터: AES-256 군사급 보안 모듈 가동")
    print("==================================================\n")

    # 1. 암호화 객체 생성 (비밀 키 자동 생성)
    aes_system = AES256Cipher()
    secret_key = aes_system.get_key_base64()

    print(f"🔑 발급된 마스터 키 (절대 유출 금지): {secret_key}\n")

    # 2. 평문 암호화 테스트
    target_message = "emergency storage door open: password is 'coffee'"
    print(f"📄 원본 데이터: {target_message}")

    encrypted_msg = aes_system.encrypt(target_message)
    print(f"🔒 AES-256 암호문: {encrypted_msg}\n")

    # 3. 암호문 복호화 테스트
    decrypted_msg = aes_system.decrypt(encrypted_msg)
    print(f"🔓 복호화된 데이터: {decrypted_msg}")

    # 검증
    if target_message == decrypted_msg:
        print("\n[SYSTEM] 무결성 검증 완료: 암/복호화가 완벽하게 수행되었습니다.")