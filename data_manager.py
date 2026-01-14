import json
import os
import sys


class DataManager:
    def __init__(self):
        # 실행 파일(.exe) 대응 경로 설정
        if getattr(sys, 'frozen', False):
            self.app_path = os.path.dirname(sys.executable)
        else:
            self.app_path = os.path.dirname(os.path.abspath(__file__))

        self.data_file = os.path.join(self.app_path, "guest_data.json")
        self.config_file = os.path.join(self.app_path, "config.json")

    # --- 데이터(하객 명단) 관리 ---
    def save_data(self, data_list):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data_list, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"데이터 저장 오류: {e}")

    def load_data(self):
        if not os.path.exists(self.data_file):
            return []
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            return []

    # --- 설정(카테고리) 관리 ---
    def load_config(self):
        """설정 파일 로드 (없으면 기본값 생성)"""
        default_config = {
            "sides": ["신랑", "신부"],
            "relations": ["친구", "친척", "직장", "가족", "지인", "기타"]
        }

        if not os.path.exists(self.config_file):
            self.save_config(default_config)
            return default_config

        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 혹시 키가 비어있을 경우를 대비해 병합
                if "sides" not in config: config["sides"] = default_config["sides"]
                if "relations" not in config: config["relations"] = default_config["relations"]
                return config
        except:
            return default_config

    def save_config(self, config):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"설정 저장 오류: {e}")