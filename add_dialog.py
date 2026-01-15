import customtkinter as ctk


class AddGuestDialog(ctk.CTkToplevel):
    def __init__(self, parent, side_list, relation_list, guest_data=None):
        super().__init__(parent)

        self.guest_data = guest_data

        self.side_list = side_list
        self.relation_list = relation_list

        title = "하객 수정" if guest_data else "새 하객 등록"
        self.title(title)

        # 창 크기 설정
        window_width = 520
        window_height = 680
        self.geometry(f"{window_width}x{window_height}")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self._init_ui()
        self._center_window(parent, window_width, window_height)

    def _center_window(self, parent, width, height):
        parent.update_idletasks()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)

        if x < 0: x = 0
        if y < 0: y = 0
        self.geometry(f"+{x}+{y}")

    def _init_ui(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # --- 1. 인적 사항 ---
        ctk.CTkLabel(self.main_frame, text="👤 인적 사항", font=("Malgun Gothic", 14, "bold"), anchor="w").pack(fill="x",
                                                                                                            pady=(
                                                                                                            0, 10))

        input_frame = ctk.CTkFrame(self.main_frame, fg_color="#f0f0f0")
        input_frame.pack(fill="x", pady=(0, 20))

        # 이름 & 소속
        row1 = ctk.CTkFrame(input_frame, fg_color="transparent")
        row1.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(row1, text="이름", width=60, anchor="w").pack(side="left")
        self.entry_name = ctk.CTkEntry(row1, placeholder_text="미기재 시 자동입력", width=100)
        self.entry_name.pack(side="left", padx=5, expand=True, fill="x")

        ctk.CTkLabel(row1, text="소속", width=40, anchor="w").pack(side="left", padx=(10, 0))
        self.entry_affil = ctk.CTkEntry(row1, placeholder_text="삼성전자", width=100)
        self.entry_affil.pack(side="left", padx=5, expand=True, fill="x")

        # 구분 & 관계
        row2 = ctk.CTkFrame(input_frame, fg_color="transparent")
        row2.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(row2, text="구분", width=60, anchor="w").pack(side="left")

        self.combo_side = ctk.CTkComboBox(row2, values=self.side_list, width=90, state="readonly")
        if self.side_list:
            self.combo_side.set(self.side_list[0])  # 첫 번째 항목 기본 선택
        self.combo_side.pack(side="left", padx=5)

        ctk.CTkLabel(row2, text="관계", width=40, anchor="w").pack(side="left", padx=(20, 0))

        self.combo_relation = ctk.CTkComboBox(row2, values=self.relation_list, width=90)
        if self.relation_list:
            self.combo_relation.set(self.relation_list[0])  # 첫 번째 항목 기본 선택
        self.combo_relation.pack(side="left", padx=5)

        # --- 2. 축의금 및 식권 ---
        ctk.CTkLabel(self.main_frame, text="💰 축의금 및 식권", font=("Malgun Gothic", 14, "bold"), anchor="w").pack(fill="x",
                                                                                                               pady=(
                                                                                                               0, 10))

        money_frame = ctk.CTkFrame(self.main_frame, fg_color="#E3F2FD")
        money_frame.pack(fill="x", pady=(0, 20))

        # 금액 입력
        m_row1 = ctk.CTkFrame(money_frame, fg_color="transparent")
        m_row1.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(m_row1, text="금액", width=40, anchor="w", font=("Malgun Gothic", 14, "bold")).pack(side="left")

        self.entry_amount = ctk.CTkEntry(m_row1, placeholder_text="0",
                                         font=("Arial", 22, "bold"),
                                         justify="right",
                                         width=160, height=45)
        self.entry_amount.pack(side="left", padx=5)
        ctk.CTkLabel(m_row1, text="원", width=20, font=("Malgun Gothic", 16, "bold")).pack(side="left")

        # 금액 퀵 버튼
        m_row2 = ctk.CTkFrame(money_frame, fg_color="transparent")
        m_row2.pack(fill="x", padx=10, pady=(0, 10))

        btn_opts = {"width": 80, "height": 40, "fg_color": "#90A4AE", "font": ("Malgun Gothic", 12, "bold")}
        ctk.CTkButton(m_row2, text="+1만", command=lambda: self.add_money(10000), **btn_opts).pack(side="left", padx=5)
        ctk.CTkButton(m_row2, text="+5만", command=lambda: self.add_money(50000), **btn_opts).pack(side="left", padx=5)
        ctk.CTkButton(m_row2, text="+10만", command=lambda: self.add_money(100000), **btn_opts).pack(side="left", padx=5)

        ctk.CTkButton(m_row2, text="C", command=lambda: self.entry_amount.delete(0, "end"),
                      width=40, height=40, fg_color="#EF5350", hover_color="#E53935",
                      font=("Arial", 12, "bold")).pack(side="right", padx=5)

        # 식권 수량
        m_row3 = ctk.CTkFrame(money_frame, fg_color="transparent")
        m_row3.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(m_row3, text="식권", width=40, anchor="w", font=("Malgun Gothic", 14, "bold")).pack(side="left")

        self.meal_var = ctk.IntVar(value=1)
        btn_minus = ctk.CTkButton(m_row3, text="-", width=45, height=45, fg_color="#B0BEC5",
                                  font=("Arial", 20, "bold"),
                                  command=lambda: self.meal_var.set(max(0, self.meal_var.get() - 1)))
        btn_minus.pack(side="left", padx=10)

        self.lbl_meal = ctk.CTkLabel(m_row3, textvariable=self.meal_var, width=60, font=("Arial", 24, "bold"))
        self.lbl_meal.pack(side="left", padx=10)

        btn_plus = ctk.CTkButton(m_row3, text="+", width=45, height=45, fg_color="#B0BEC5",
                                 font=("Arial", 20, "bold"),
                                 command=lambda: self.meal_var.set(self.meal_var.get() + 1))
        btn_plus.pack(side="left", padx=10)

        # --- 3. 비고 ---
        ctk.CTkLabel(self.main_frame, text="📝 비고 (메모)", font=("Malgun Gothic", 12), anchor="w",
                     text_color="gray").pack(fill="x", pady=(0, 5))
        self.entry_note = ctk.CTkTextbox(self.main_frame, height=80)
        self.entry_note.pack(fill="x", pady=(0, 20))

        # --- 하단 버튼 ---
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", side="bottom")

        ctk.CTkButton(btn_frame, text="취소", fg_color="gray", hover_color="#666",
                      font=("Malgun Gothic", 14, "bold"),
                      width=100, height=55, command=self.destroy).pack(side="left", expand=True, padx=10)

        ctk.CTkButton(btn_frame, text="저장 하기", fg_color="#2E7D32", hover_color="#1B5E20",
                      font=("Malgun Gothic", 14, "bold"),
                      width=100, height=55, command=self.save_data).pack(side="left", expand=True, padx=10)

        # 데이터 채우기 (수정 모드)
        if self.guest_data:
            self.entry_name.insert(0, self.guest_data.get("name", ""))
            self.entry_affil.insert(0, self.guest_data.get("affiliation", ""))

            # 저장된 값이 콤보박스 목록에 없으면(삭제된 경우) 기본값 사용
            saved_side = self.guest_data.get("side", "")
            if saved_side in self.side_list:
                self.combo_side.set(saved_side)

            saved_relation = self.guest_data.get("relation", "")
            if saved_relation in self.relation_list:
                self.combo_relation.set(saved_relation)

            amt = self.guest_data.get("amount", 0)
            if amt > 0: self.entry_amount.insert(0, str(amt))
            self.meal_var.set(self.guest_data.get("meal", 1))
            self.entry_note.insert("1.0", self.guest_data.get("note", ""))

    def add_money(self, amount):
        try:
            current = self.entry_amount.get().replace(",", "")
            current = int(current) if current else 0
            self.entry_amount.delete(0, "end")
            self.entry_amount.insert(0, str(current + amount))
        except ValueError:
            pass

    def save_data(self):
        name = self.entry_name.get().strip()
        side = self.combo_side.get()
        relation = self.combo_relation.get()
        affiliation = self.entry_affil.get().strip()
        note = self.entry_note.get("1.0", "end-1c").strip()

        raw_amount = self.entry_amount.get().replace(",", "")
        try:
            amount = int(raw_amount) if raw_amount else 0
        except ValueError:
            amount = 0
        meal = self.meal_var.get()

        # result
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