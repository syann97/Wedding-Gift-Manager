import customtkinter as ctk
from tkinter import messagebox


class AddGuestDialog(ctk.CTkToplevel):
    def __init__(self, parent, side_list, relation_list, guest_data=None):
        super().__init__(parent)

        # [Logic] 데이터 수신
        self.guest_data = guest_data
        self.side_list = side_list
        self.relation_list = relation_list
        self.result_data = None

        # 타이틀 설정
        title_text = "하객 정보 수정" if self.guest_data else "새 하객 등록"
        self.title(title_text)

        # [UI] 창 크기 및 설정 (1번 스타일)
        window_width = 520
        window_height = 680
        self.geometry(f"{window_width}x{window_height}")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # 폰트 스타일
        self.font_header = ("Malgun Gothic", 16, "bold")
        self.font_label = ("Malgun Gothic", 13)
        self.font_input = ("Malgun Gothic", 13)

        self._init_ui()

        # 데이터 채우기 (수정 모드)
        if self.guest_data:
            self._populate_data()
            self.btn_save.configure(text="수정 완료", fg_color="#1E88E5", hover_color="#1976D2")

        self._center_window(parent, window_width, window_height)
        self.focus_force()

    def _init_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # ================= [섹션 1] 인적 사항 =================
        info_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        info_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(info_frame, text="👤 인적 사항", font=self.font_header).pack(anchor="w", padx=20, pady=(20, 15))

        row1 = ctk.CTkFrame(info_frame, fg_color="transparent")
        row1.pack(fill="x", padx=20, pady=(0, 15))

        # 이름 (필수 표시 * 는 유지하되, 로직상 공백 허용)
        ctk.CTkLabel(row1, text="이름", font=self.font_label).pack(side="left", padx=(0, 10))
        self.entry_name = ctk.CTkEntry(row1, width=130, font=self.font_input, placeholder_text="예: 홍길동")
        self.entry_name.pack(side="left")

        ctk.CTkLabel(row1, text="소속", font=self.font_label).pack(side="left", padx=(20, 10))
        self.entry_affil = ctk.CTkEntry(row1, width=150, font=self.font_input, placeholder_text="예: 삼성전자")
        self.entry_affil.pack(side="left", fill="x", expand=True)

        row2 = ctk.CTkFrame(info_frame, fg_color="transparent")
        row2.pack(fill="x", padx=20, pady=(0, 20))

        ctk.CTkLabel(row2, text="구분", font=self.font_label).pack(side="left", padx=(0, 10))

        self.combo_side = ctk.CTkComboBox(row2, values=self.side_list, width=130, font=self.font_input)
        if self.side_list:
            self.combo_side.set(self.side_list[0])
        self.combo_side.pack(side="left")

        ctk.CTkLabel(row2, text="관계", font=self.font_label).pack(side="left", padx=(20, 10))

        self.combo_rel = ctk.CTkComboBox(row2, values=self.relation_list, width=120, font=self.font_input)
        if self.relation_list:
            self.combo_rel.set(self.relation_list[0])
        self.combo_rel.pack(side="left", fill="x", expand=True)

        # ================= [섹션 2] 축의금 및 식권 =================
        money_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color=("#E3F2FD", "#1e2a36"))
        money_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(money_frame, text="💰 축의금 및 식권", font=self.font_header, text_color=("#1565C0", "#64B5F6")).pack(
            anchor="w", padx=20, pady=(20, 10))

        money_row = ctk.CTkFrame(money_frame, fg_color="transparent")
        money_row.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(money_row, text="금액", font=self.font_label).pack(side="left", padx=(0, 10))

        self.entry_amount = ctk.CTkEntry(money_row, font=("Roboto", 20, "bold"), justify="right", width=180, height=35)
        self.entry_amount.insert(0, "0")
        self.entry_amount.pack(side="left")
        ctk.CTkLabel(money_row, text="원", font=self.font_label).pack(side="left", padx=(10, 0))

        btn_row = ctk.CTkFrame(money_frame, fg_color="transparent")
        btn_row.pack(fill="x", padx=20, pady=(5, 15))

        def make_add_btn(amt, label):
            return ctk.CTkButton(btn_row, text=label, width=60, height=30,
                                 fg_color="#90A4AE", hover_color="#607D8B",
                                 command=lambda: self.add_money(amt))

        make_add_btn(10000, "+1만").pack(side="left", padx=(0, 5))
        make_add_btn(50000, "+5만").pack(side="left", padx=5)
        make_add_btn(100000, "+10만").pack(side="left", padx=5)

        ctk.CTkButton(btn_row, text="C", width=40, height=30, fg_color="#EF5350", hover_color="#C62828",
                      command=lambda: self._set_money(0)).pack(side="right")

        meal_row = ctk.CTkFrame(money_frame, fg_color="transparent")
        meal_row.pack(fill="x", padx=20, pady=(5, 20))

        ctk.CTkLabel(meal_row, text="식권", font=self.font_label).pack(side="left", padx=(0, 10))

        counter_box = ctk.CTkFrame(meal_row, fg_color="transparent")
        counter_box.pack(side="left")

        self.meal_var = ctk.IntVar(value=1)

        ctk.CTkButton(counter_box, text="-", width=35, height=35, fg_color="#B0BEC5", text_color="black",
                      command=lambda: self.meal_var.set(max(0, self.meal_var.get() - 1))).pack(side="left")

        self.lbl_ticket = ctk.CTkLabel(counter_box, textvariable=self.meal_var, font=("Roboto", 20, "bold"), width=50)
        self.lbl_ticket.pack(side="left", padx=5)

        ctk.CTkButton(counter_box, text="+", width=35, height=35, fg_color="#B0BEC5", text_color="black",
                      command=lambda: self.meal_var.set(self.meal_var.get() + 1)).pack(side="left")

        # ================= [섹션 3] 비고 =================
        note_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        note_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(note_frame, text="📝 비고 (메모)", font=self.font_label).pack(anchor="w", padx=20, pady=(15, 5))

        self.entry_note = ctk.CTkTextbox(note_frame, height=70, font=self.font_input)
        self.entry_note.pack(fill="x", padx=20, pady=(0, 20))

        # ================= [버튼] 하단 액션 =================
        action_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        action_frame.pack(fill="x", pady=(10, 0))

        self.btn_cancel = ctk.CTkButton(action_frame, text="취소", height=45,
                                        fg_color="#cfd8dc", text_color="black", hover_color="#b0bec5",
                                        font=self.font_header,
                                        command=self.destroy)
        self.btn_cancel.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # [요청사항 2 반영] 색상을 이미지와 같은 #2EB086으로 변경
        self.btn_save = ctk.CTkButton(action_frame, text="저장 하기", height=45,
                                      fg_color="#2EB086", hover_color="#219F79", font=self.font_header,
                                      command=self.save_data)
        self.btn_save.pack(side="right", fill="x", expand=True, padx=(10, 0))

        self.bind('<Return>', lambda e: self.save_data())

    def _populate_data(self):
        data = self.guest_data
        if not data: return

        self.entry_name.delete(0, "end")
        self.entry_name.insert(0, data.get('name', ''))

        self.entry_affil.delete(0, "end")
        self.entry_affil.insert(0, data.get('affiliation', ''))

        side = data.get('side', '')
        if side in self.side_list:
            self.combo_side.set(side)

        rel = data.get('relation', '')
        if rel in self.relation_list:
            self.combo_rel.set(rel)

        amount = data.get('amount', 0)
        self._set_money(amount)

        self.meal_var.set(data.get('meal', 1))

        self.entry_note.delete("1.0", "end")
        self.entry_note.insert("1.0", data.get('note', ''))

    def _get_current_amount(self):
        try:
            val = self.entry_amount.get().replace(",", "")
            return int(val) if val else 0
        except ValueError:
            return 0

    def add_money(self, amount):
        current = self._get_current_amount()
        self._set_money(current + amount)

    def _set_money(self, value):
        self.entry_amount.delete(0, "end")
        self.entry_amount.insert(0, f"{value:,}")

    def _center_window(self, parent, width, height):
        """창을 모니터 화면의 정중앙에 배치"""
        self.update_idletasks()  # 현재 창의 크기 정보를 최신화

        # 1. 사용자의 모니터 해상도 가져오기
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # 2. 정중앙 좌표 계산 (화면크기/2 - 창크기/2)
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        # 3. Y축 보정 (너무 정중앙이면 시각적으로 처져 보일 수 있어 살짝만 위로 올림)
        # 원하시면 '- 50' 부분을 지우셔도 됩니다.
        y = y - 50

        # 4. 화면 밖으로 나가는 것 방지 (안전장치)
        if x < 0: x = 0
        if y < 0: y = 0

        # 5. 위치 적용
        self.geometry(f"{width}x{height}+{x}+{y}")

    def save_data(self):
        name = self.entry_name.get().strip()

        # [요청사항 1 반영] 이름 공백 검사 로직 제거 (경고창 없이 진행)

        side = self.combo_side.get()
        relation = self.combo_rel.get()
        affiliation = self.entry_affil.get().strip()
        note = self.entry_note.get("1.0", "end-1c").strip()

        amount = self._get_current_amount()
        meal = self.meal_var.get()

        result = {
            "name": name,
            "amount": amount,
            "side": side,
            "relation": relation,
            "affiliation": affiliation,
            "meal": meal,
            "note": note
        }

        self.result_data = result
        self.destroy()