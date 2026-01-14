import json
import os
import sys


class DataManager:
    def __init__(self, filename="guest_data.json"):
        # 1. 현재 실행 중인 파일의 절대 경로 찾기 (PyInstaller 대응 핵심 코드)
        if getattr(sys, 'frozen', False):
            # exe로 실행 중일 때: 실행 파일이 있는 폴더
            application_path = os.path.dirname(sys.executable)
        else:
            # 스크립트로 실행 중일 때: 현재 파이썬 파일이 있는 폴더
            application_path = os.path.dirname(os.path.abspath(__file__))

        # 2. 경로와 파일명 합치기
        self.filepath = os.path.join(application_path, filename)

    def save_data(self, data_list):
        """
        데이터 리스트를 JSON 파일로 저장
        :param data_list: 딕셔너리들의 리스트 (예: [{'name': '홍길동', ...}, ...])
        """
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                # ensure_ascii=False: 한글이 깨지지 않고 그대로 저장됨 (필수!)
                # indent=4: 사람이 보기 좋게 줄바꿈/들여쓰기 적용
                json.dump(data_list, f, ensure_ascii=False, indent=4)
            print(f"저장 완료: {self.filepath}")
        except Exception as e:
            print(f"저장 중 오류 발생: {e}")

    def load_data(self):
        """
        JSON 파일에서 데이터를 읽어옴
        :return: 데이터 리스트 (파일이 없으면 빈 리스트 반환)
        """
        if not os.path.exists(self.filepath):
            return []  # 파일이 없으면 빈 리스트 리턴

        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"불러오기 오류: {e}")
            return []  # 오류 발생 시 빈 리스트 리턴 (프로그램 멈춤 방지)


# 사용 예시 (테스트용)
if __name__ == "__main__":
    manager = DataManager()

    # 1. 데이터 저장 테스트
    sample_data = [
        {"name": "홍길동", "amount": 100000, "side": "신랑", "relation": "친구"},
        {"name": "김철수", "amount": 50000, "side": "신부", "relation": "사촌"}
    ]
    manager.save_data(sample_data)

    # 2. 데이터 불러오기 테스트
    loaded_data = manager.load_data()
    print("불러온 데이터:", loaded_data)