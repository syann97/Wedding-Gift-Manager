import customtkinter as ctk
from tkinter import messagebox


class SettingsDialog(ctk.CTkToplevel):
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.title("카테고리 설정")
        self.geometry("400x500")
        self.resizable(False, False)

        # 모달 설정
        self.transient(parent)
        self.grab_set()

        self.db = data_manager
        self.config = self.db.load_config()

        self._init_ui()
        self._center_window(parent)

    def _init_ui(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)

        self.tab_relation = self.tabview.add("관계 설정")
        self.tab_side = self.tabview.add("구분(대상) 설정")

        self._create_editor(self.tab_relation, "relations")
        self._create_editor(self.tab_side, "sides")

    def _create_editor(self, parent, key):
        # 스크롤 가능한 목록 영역
        frame_list = ctk.CTkScrollableFrame(parent, height=200)
        frame_list.pack(fill="x", padx=10, pady=10)

        # 입력 영역
        input_frame = ctk.CTkFrame(parent, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=(10, 0))

        entry = ctk.CTkEntry(input_frame, placeholder_text="새 항목 입력")
        entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        # 내부 함수: 목록 새로고침
        def refresh_list():
            for widget in frame_list.winfo_children():
                widget.destroy()

            for item in self.config[key]:
                row = ctk.CTkFrame(frame_list, fg_color="transparent")
                row.pack(fill="x", pady=2)

                lbl = ctk.CTkLabel(row, text=item, anchor="w")
                lbl.pack(side="left", padx=5)

                # 삭제 버튼 (lambda 주의)
                btn_del = ctk.CTkButton(row, text="삭제", width=40, height=20, fg_color="#EF5350",
                                        command=lambda i=item: delete_item(i))
                btn_del.pack(side="right")

        # 내부 함수: 삭제
        def delete_item(item):
            if len(self.config[key]) <= 1:
                messagebox.showwarning("경고", "최소 1개의 항목은 있어야 합니다.")
                return
            if item in self.config[key]:
                self.config[key].remove(item)
                self.db.save_config(self.config)
                refresh_list()

        # 내부 함수: 추가
        def add_item():
            text = entry.get().strip()
            if not text: return
            if text in self.config[key]:
                messagebox.showwarning("중복", "이미 존재하는 항목입니다.")
                return

            self.config[key].append(text)
            self.db.save_config(self.config)
            entry.delete(0, "end")
            refresh_list()

        btn_add = ctk.CTkButton(input_frame, text="추가", width=60, command=add_item)
        btn_add.pack(side="right")

        # 엔터키로 추가
        entry.bind('<Return>', lambda e: add_item())

        refresh_list()  # 초기 로딩

    def _center_window(self, parent):
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (400 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (500 // 2)
        self.geometry(f"+{x}+{y}")