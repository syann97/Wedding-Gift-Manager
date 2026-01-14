import customtkinter as ctk
from tkinter import messagebox


class AddGuestDialog(ctk.CTkToplevel):
    def __init__(self, parent, initial_data=None):
        super().__init__(parent)

        # 1. 수정 모드인지 확인
        self.is_edit_mode = initial_data is not None
        self.initial_data = initial_data

        # 2. 타이틀 설정
        title_text = "하객 정보 수정" if self.is_edit_mode else "새 하객 등록"
        self.title(title_text)

        self.geometry("520x680")
        self.resizable(False, False)

        # 모달 설정 (부모 창 제어 잠금)
        self.transient(parent)
        self.grab_set()
        self.focus_force()

        # 결과 데이터 저장 변수
        self.guest_data = None

        # 폰트 설정
        self.font_header = ("Malgun Gothic", 16, "bold")
        self.font_label = ("Malgun Gothic", 13)
        self.font_input = ("Malgun Gothic", 13)

        # UI 그리기
        self._init_ui()

        # ★ 수정 모드일 경우 기존 데이터 채워 넣기
        if self.is_edit_mode:
            self._populate_data()
            # 저장 버튼을 파란색 '수정 완료' 버튼으로 변경
            self.btn_save.configure(text="수정 완료", fg_color="#1E88E5", hover_color="#1976D2")

        self._center_window(parent)

    def _init_ui(self):
        # 전체 컨테이너
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # --- [섹션 1] 인적 사항 ---
        info_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        info_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(info_frame, text="👤 인적 사항", font=self.font_header).pack(anchor="w", padx=20, pady=(20, 15))

        # [Row 1] 이름 & 소속
        row1 = ctk.CTkFrame(info_frame, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=(0, 15))

        # 이름
        ctk.CTkLabel(row1, text="이름 *", font=self.font_label).pack(side="left", padx=(0, 10))
        self.entry_name = ctk.CTkEntry(row1, width=130, font=self.font_input, placeholder_text="예: 홍길동")
        self.entry_name.pack(side="left")

        # 소속
        ctk.CTkLabel(row1, text="소속", font=self.font_label).pack(side="left", padx=(20, 10))
        self.entry_affil = ctk.CTkEntry(row1, width=150, font=self.font_input, placeholder_text="예: 삼성전자")
        self.entry_affil.pack(side="left", fill="x", expand=True)

        # [Row 2] 구분 & 관계
        row2 = ctk.CTkFrame(info_frame, fg_color="transparent")
        row2.pack(fill="x", padx=20, pady=(0, 20))

        # 구분 (신랑/신부)
        ctk.CTkLabel(row2, text="구분", font=self.font_label).pack(side="left", padx=(0, 10))
        self.seg_side = ctk.CTkSegmentedButton(row2, values=["신랑", "신부"], width=130, font=("Malgun Gothic", 12, "bold"))
        self.seg_side.set("신랑")
        self.seg_side.pack(side="left")

        # 관계
        ctk.CTkLabel(row2, text="관계", font=self.font_label).pack(side="left", padx=(20, 10))
        self.combo_rel = ctk.CTkComboBox(row2, values=["친구", "친척", "직장", "가족", "지인", "기타"],
                                         width=120, font=self.font_input)
        self.combo_rel.set("친구")
        self.combo_rel.pack(side="left", fill="x", expand=True)

        # --- [섹션 2] 축의금 및 식권 ---
        money_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color=("#E3F2FD", "#1e2a36"))
        money_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(money_frame, text="💰 축의금 및 식권", font=self.font_header, text_color=("#1565C0", "#64B5F6")).pack(
            anchor="w", padx=20, pady=(20, 10))

        # 금액 입력 Row
        money_row = ctk.CTkFrame(money_frame, fg_color="transparent")
        money_row.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(money_row, text="금액", font=self.font_label).pack(side="left", padx=(0, 10))
        self.entry_amount = ctk.CTkEntry(money_row, font=("Roboto", 20, "bold"), justify="right", width=180, height=35)
        self.entry_amount.insert(0, "0")
        self.entry_amount.pack(side="left")
        ctk.CTkLabel(money_row, text="원", font=self.font_label).pack(side="left", padx=(10, 0))

        # 간편 버튼 Row
        btn_row = ctk.CTkFrame(money_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=20, pady=(5, 15))

        def make_add_btn(amt, label):
            return ctk.CTkButton(btn_row, text=label, width=60, height=30,
                                 fg_color="#90A4AE", hover_color="#607D8B",
                                 command=lambda: self._add_money(amt))

        make_add_btn(10000, "+1만").pack(side="left", padx=(0, 5))
        make_add_btn(50000, "+5만").pack(side="left", padx=5)
        make_add_btn(100000, "+10만").pack(side="left", padx=5)

        ctk.CTkButton(btn_row, text="C", width=40, height=30, fg_color="#EF5350", hover_color="#C62828",
                      command=lambda: self._set_money(0)).pack(side="right")

        # 식권 Row
        meal_row = ctk.CTkFrame(money_frame, fg_color="transparent")
        meal_row.pack(fill="x", padx=20, pady=(5, 20))

        ctk.CTkLabel(meal_row, text="식권", font=self.font_label).pack(side="left", padx=(0, 10))

        counter_box = ctk.CTkFrame(meal_row, fg_color="transparent")
        counter_box.pack(side="left")

        ctk.CTkButton(counter_box, text="-", width=35, height=35, fg_color="#B0BEC5", text_color="black",
                      command=lambda: self._change_ticket(-1)).pack(side="left")

        self.lbl_ticket = ctk.CTkLabel(counter_box, text="1", font=("Roboto", 20, "bold"), width=50)
        self.lbl_ticket.pack(side="left", padx=5)

        ctk.CTkButton(counter_box, text="+", width=35, height=35, fg_color="#B0BEC5", text_color="black",
                      command=lambda: self._change_ticket(1)).pack(side="left")

        # --- [섹션 3] 비고 및 버튼 ---
        note_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        note_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(note_frame, text="📝 비고 (메모)", font=self.font_label).pack(anchor="w", padx=20, pady=(15, 5))
        self.entry_note = ctk.CTkTextbox(note_frame, height=70, font=self.font_input)
        self.entry_note.pack(fill="x", padx=20, pady=(0, 20))

        # 하단 액션 버튼
        action_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        action_frame.pack(fill="x", pady=(10, 0))

        self.btn_cancel = ctk.CTkButton(action_frame, text="취소", height=45,
                                        fg_color="#cfd8dc", text_color="black", hover_color="#b0bec5",
                                        font=self.font_header,
                                        command=self.destroy)
        self.btn_cancel.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_save = ctk.CTkButton(action_frame, text="저장 하기", height=45,
                                      fg_color="#2EB086", hover_color="#219F79", font=self.font_header,
                                      command=self.save_guest)
        self.btn_save.pack(side="right", fill="x", expand=True, padx=(10, 0))

        self.bind('<Return>', lambda e: self.save_guest())

    # --- 데이터 로드 (수정 모드용) ---
    def _populate_data(self):
        """기존 데이터를 입력창에 채워넣기"""
        data = self.initial_data

        # 이름
        self.entry_name.delete(0, "end")
        self.entry_name.insert(0, data.get('name', ''))

        # 소속
        self.entry_affil.delete(0, "end")
        self.entry_affil.insert(0, data.get('affiliation', ''))

        # 구분 (신랑/신부)
        self.seg_side.set(data.get('side', '신랑'))

        # 관계
        self.combo_rel.set(data.get('relation', '친구'))

        # 금액 (콤마 포맷팅 포함)
        amount = data.get('amount', 0)
        self._set_money(amount)

        # 식권
        self.lbl_ticket.configure(text=str(data.get('meal', 1)))

        # 비고 (Textbox는 인덱스가 "1.0"부터 시작)
        self.entry_note.delete("1.0", "end")
        self.entry_note.insert("1.0", data.get('note', ''))

    # --- 내부 로직 ---
    def _get_current_amount(self):
        try:
            val = self.entry_amount.get().replace(",", "")
            return int(val) if val else 0
        except ValueError:
            return 0

    def _add_money(self, amount):
        current = self._get_current_amount()
        self._set_money(current + amount)

    def _set_money(self, value):
        self.entry_amount.delete(0, "end")
        self.entry_amount.insert(0, f"{value:,}")

    def _change_ticket(self, delta):
        current = int(self.lbl_ticket.cget("text"))
        new_val = max(0, current + delta)
        self.lbl_ticket.configure(text=str(new_val))

    def _center_window(self, parent):
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (520 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (680 // 2)
        self.geometry(f"+{x}+{y}")

    def save_guest(self):
        name = self.entry_name.get().strip()
        if not name:
            messagebox.showwarning("입력 오류", "이름은 필수 입력 항목입니다.")
            self.entry_name.focus_set()
            return

        self.guest_data = {
            "name": name,
            "affiliation": self.entry_affil.get().strip(),
            "side": self.seg_side.get(),
            "relation": self.combo_rel.get(),
            "amount": self._get_current_amount(),
            "meal": int(self.lbl_ticket.cget("text")),
            "note": self.entry_note.get("1.0", "end").strip()
        }
        self.destroy()