import tkinter.ttk as ttk
import customtkinter as ctk
from data_manager import DataManager
from add_dialog import AddGuestDialog
from tkinter import messagebox

# --- 초기 설정 ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


class WeddingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. 윈도우 설정
        self.title("안해리 축의금 정산 매니저 Pro (Full Zebra Style)")
        self.geometry("1280x800")
        self.minsize(1000, 700)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.font_bold = ("Malgun Gothic", 12, "bold")
        self.font_body = ("Malgun Gothic", 12)

        # 2. DB 연결 및 데이터 로드
        self.db = DataManager()
        self.guest_list = self.db.load_data()

        # (테스트용) 데이터 없으면 샘플 생성
        if not self.guest_list:
            self.guest_list = [
                {"name": "홍길동", "amount": 100000, "side": "신랑", "relation": "친구", "affiliation": "삼성전자", "meal": 1,
                 "note": "축하해"},
                {"name": "김철수", "amount": 50000, "side": "신부", "relation": "친척", "affiliation": "이모부", "meal": 2,
                 "note": ""}
            ]
            self.db.save_data(self.guest_list)

        # UI 배치
        self.create_top_frame()
        self.create_list_frame()
        self.create_bottom_dashboard()

        # 시작 시 화면 갱신
        self.refresh_ui()

    def create_top_frame(self):
        """상단 검색 및 액션 버튼"""
        self.top_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        self.title_label = ctk.CTkLabel(self.top_frame, text="Wedding Guest Manager",
                                        font=("Roboto Medium", 20), text_color=("gray30", "gray70"))
        self.title_label.pack(side="left", padx=(10, 30))

        # 콤보박스 & 입력창
        self.search_combo = ctk.CTkComboBox(self.top_frame, values=["이름", "소속", "관계"],
                                            width=100, height=35, font=self.font_body)
        self.search_combo.set("이름")
        self.search_combo.pack(side="left", padx=5)

        self.search_entry = ctk.CTkEntry(self.top_frame, placeholder_text="검색어를 입력하세요...",
                                         width=300, height=35, font=self.font_body)
        self.search_entry.pack(side="left", padx=5)

        self.btn_search = ctk.CTkButton(self.top_frame, text="🔍 검색", width=80, height=35,
                                        fg_color="#546e7a", hover_color="#455a64", font=self.font_bold)
        self.btn_search.pack(side="left", padx=5)

        # 추가 버튼
        self.btn_add = ctk.CTkButton(self.top_frame, text="+ 하객 추가", width=120, height=35,
                                     fg_color="#2EB086", hover_color="#219F79", font=self.font_bold,
                                     command=self.open_add_dialog)
        self.btn_add.pack(side="right", padx=5)

        # 삭제 버튼
        self.btn_delete = ctk.CTkButton(self.top_frame, text="- 선택 삭제", width=120, height=35,
                                        fg_color="#D84315", hover_color="#BF360C", font=self.font_bold,
                                        command=self.delete_guest)
        self.btn_delete.pack(side="right", padx=5)

    def create_list_frame(self):
        """중앙 리스트 UI"""
        self.list_frame = ctk.CTkFrame(self, corner_radius=15)
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.list_frame.grid_rowconfigure(1, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)

        self.lbl_list_title = ctk.CTkLabel(self.list_frame, text="하객 명단 리스트",
                                           font=("Malgun Gothic", 18, "bold"))
        self.lbl_list_title.grid(row=0, column=0, sticky="w", padx=20, pady=(15, 10))

        style = ttk.Style()
        style.theme_use("clam")

        # 스타일 설정
        bg_color = "white"
        header_bg = "#343a40"
        header_fg = "white"
        row_selected = "#3B8ED0"

        style.configure("Treeview", background=bg_color, fieldbackground=bg_color, foreground="black",
                        rowheight=35, borderwidth=0, font=("Malgun Gothic", 11))
        style.configure("Treeview.Heading", background=header_bg, foreground=header_fg, relief="flat",
                        font=("Malgun Gothic", 11, "bold"))
        style.map("Treeview", background=[('selected', row_selected)], foreground=[('selected', 'white')])

        columns = ("No", "Name", "Amount", "GuestOf", "Relation", "Affiliation", "Meal", "Note")
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show="headings", style="Treeview")

        headers = [
            ("No", "No", "center", 50),
            ("Name", "이름", "center", 100),
            ("Amount", "금액 (원)", "e", 120),
            ("GuestOf", "대상", "center", 80),
            ("Relation", "관계", "center", 80),
            ("Affiliation", "소속", "w", 150),
            ("Meal", "식권", "center", 60),
            ("Note", "비고", "w", 250)
        ]

        for col, text, anchor, width in headers:
            self.tree.heading(col, text=text)
            self.tree.column(col, anchor=anchor, width=width)

        self.tree.tag_configure("evenrow", background="#f8f9fa")
        self.tree.tag_configure("oddrow", background="white")

        self.scrollbar = ctk.CTkScrollbar(self.list_frame, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)

        self.tree.grid(row=1, column=0, sticky="nsew", padx=(20, 5), pady=(0, 20))
        self.scrollbar.grid(row=1, column=1, sticky="ns", padx=(0, 20), pady=(0, 20))

        # ★ 더블 클릭 이벤트 바인딩 (이제 정상 작동합니다)
        self.tree.bind("<Double-1>", self.edit_guest)

    def create_bottom_dashboard(self):
        """하단 통계 대시보드 UI"""
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)

        # 왼쪽: 상세 분류
        self.stats_detail_frame = ctk.CTkFrame(self.bottom_frame, corner_radius=15, border_width=1, border_color="#ddd")
        self.stats_detail_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(self.stats_detail_frame, text="그룹별 상세 통계", font=("Malgun Gothic", 14, "bold")).pack(pady=10)

        mini_cols = ("Group", "Count", "Sum", "Meal")
        self.mini_tree = ttk.Treeview(self.stats_detail_frame, columns=mini_cols, show="headings", height=5)

        self.mini_tree.heading("Group", text="분류");
        self.mini_tree.column("Group", anchor="center", width=80)
        self.mini_tree.heading("Count", text="인원");
        self.mini_tree.column("Count", anchor="center", width=60)
        self.mini_tree.heading("Sum", text="합계 (원)");
        self.mini_tree.column("Sum", anchor="e", width=100)
        self.mini_tree.heading("Meal", text="식권");
        self.mini_tree.column("Meal", anchor="center", width=60)

        self.mini_tree.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        self.mini_tree.tag_configure("evenrow", background="#f8f9fa")
        self.mini_tree.tag_configure("oddrow", background="white")

        # 오른쪽: 요약 카드
        self.summary_frame = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        self.summary_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self.summary_frame.grid_columnconfigure(0, weight=1)
        self.summary_frame.grid_columnconfigure(1, weight=1)

        self.lbl_total_people = self.create_card(self.summary_frame, 0, 0, "전체 인원", "0 명", "#3B8ED0")
        self.lbl_total_meal = self.create_card(self.summary_frame, 0, 1, "전체 식권", "0 장", "#2CC985")

        total_card = ctk.CTkFrame(self.summary_frame, corner_radius=15, fg_color="#E3F2FD", border_width=0)
        total_card.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(total_card, text="총 정산 금액", font=("Malgun Gothic", 14, "bold"), text_color="#1565C0").pack(
            side="left", padx=20)
        self.lbl_total_money = ctk.CTkLabel(total_card, text="0 원", font=("Roboto", 28, "bold"), text_color="#0D47A1")
        self.lbl_total_money.pack(side="right", padx=20)

    def create_card(self, parent, row, col, title, initial_value, icon_color):
        card = ctk.CTkFrame(parent, corner_radius=15, fg_color=("white", "#333333"), border_width=2,
                            border_color="#eee")
        card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

        bar = ctk.CTkFrame(card, width=5, fg_color=icon_color, corner_radius=0)
        bar.pack(side="left", fill="y", padx=(0, 10))

        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, pady=10)

        ctk.CTkLabel(content, text=title, font=("Malgun Gothic", 12), text_color="gray").pack(anchor="w")
        value_label = ctk.CTkLabel(content, text=initial_value, font=("Roboto Medium", 20), text_color="black")
        value_label.pack(anchor="w")
        return value_label

    def refresh_ui(self):
        """데이터 갱신 및 UI 업데이트"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        total_count = 0
        total_money = 0
        total_meal = 0
        groom_stats = {"count": 0, "money": 0, "meal": 0}
        bride_stats = {"count": 0, "money": 0, "meal": 0}

        for i, guest in enumerate(self.guest_list):
            name = guest.get("name", "")
            amount = guest.get("amount", 0)
            side = guest.get("side", "")
            relation = guest.get("relation", "")
            affiliation = guest.get("affiliation", "")
            meal = guest.get("meal", 0)
            note = guest.get("note", "")

            total_count += 1
            total_money += amount
            total_meal += meal

            if side == "신랑":
                groom_stats["count"] += 1
                groom_stats["money"] += amount
                groom_stats["meal"] += meal
            elif side == "신부":
                bride_stats["count"] += 1
                bride_stats["money"] += amount
                bride_stats["meal"] += meal

            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=(
                i + 1, name, f"{amount:,}", side, relation, affiliation, meal, note
            ), tags=(tag,))

        for item in self.mini_tree.get_children():
            self.mini_tree.delete(item)

        self.mini_tree.insert("", "end", values=(
        "신랑측", f"{groom_stats['count']}명", f"{groom_stats['money']:,}", f"{groom_stats['meal']}"), tags=("evenrow",))
        self.mini_tree.insert("", "end", values=(
        "신부측", f"{bride_stats['count']}명", f"{bride_stats['money']:,}", f"{bride_stats['meal']}"), tags=("oddrow",))

        self.lbl_total_people.configure(text=f"{total_count} 명")
        self.lbl_total_meal.configure(text=f"{total_meal} 장")
        self.lbl_total_money.configure(text=f"{total_money:,} 원")

    def open_add_dialog(self):
        dialog = AddGuestDialog(self)
        self.wait_window(dialog)
        if dialog.guest_data:
            self.guest_list.append(dialog.guest_data)
            self.db.save_data(self.guest_list)
            self.refresh_ui()
            print(f"하객 추가됨: {dialog.guest_data['name']}")

    def delete_guest(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("선택 없음", "삭제할 하객을 목록에서 선택해주세요.")
            return

        count = len(selected_items)
        if not messagebox.askyesno("삭제 확인", f"선택한 {count}명의 하객 정보를 정말 삭제하시겠습니까?\n(이 작업은 되돌릴 수 없습니다.)"):
            return

        indices_to_delete = set()
        for item in selected_items:
            values = self.tree.item(item)['values']
            if values:
                real_index = int(values[0]) - 1
                indices_to_delete.add(real_index)

        new_guest_list = []
        for i, guest in enumerate(self.guest_list):
            if i not in indices_to_delete:
                new_guest_list.append(guest)

        self.guest_list = new_guest_list
        self.db.save_data(self.guest_list)
        self.refresh_ui()
        print(f"{count}명 삭제 완료")

    # ★ 수정: 들여쓰기를 맞춰서 클래스 메서드로 꺼냈습니다.
    def edit_guest(self, event):
        """리스트 더블 클릭 시 수정 창 띄우기"""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        values = self.tree.item(selected_item)['values']
        if not values:
            return

        # 화면의 No는 1부터 시작하므로 1을 빼야 실제 인덱스
        list_index = int(values[0]) - 1

        # 인덱스 범위 안전장치 (혹시 모를 에러 방지)
        if list_index < 0 or list_index >= len(self.guest_list):
            return

        target_data = self.guest_list[list_index]

        dialog = AddGuestDialog(self, initial_data=target_data)
        self.wait_window(dialog)

        if dialog.guest_data:
            self.guest_list[list_index] = dialog.guest_data
            self.db.save_data(self.guest_list)
            self.refresh_ui()
            print(f"수정 완료: {dialog.guest_data['name']}")


if __name__ == "__main__":
    app = WeddingApp()
    app.mainloop()