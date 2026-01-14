import tkinter.ttk as ttk
import customtkinter as ctk

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

        # UI 배치
        self.create_top_frame()
        self.create_list_frame()
        self.create_bottom_dashboard()

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

        self.btn_add = ctk.CTkButton(self.top_frame, text="+ 하객 추가", width=120, height=35,
                                     fg_color="#2EB086", hover_color="#219F79", font=self.font_bold)
        self.btn_add.pack(side="right", padx=5)

        self.btn_delete = ctk.CTkButton(self.top_frame, text="- 선택 삭제", width=120, height=35,
                                        fg_color="#D84315", hover_color="#BF360C", font=self.font_bold)
        self.btn_delete.pack(side="right", padx=5)

    def create_list_frame(self):
        """중앙 리스트 (교차 채색 적용)"""
        self.list_frame = ctk.CTkFrame(self, corner_radius=15)
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.list_frame.grid_rowconfigure(1, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)

        self.lbl_list_title = ctk.CTkLabel(self.list_frame, text="하객 명단 리스트",
                                           font=("Malgun Gothic", 18, "bold"))
        self.lbl_list_title.grid(row=0, column=0, sticky="w", padx=20, pady=(15, 10))

        # 스타일 설정
        style = ttk.Style()
        style.theme_use("clam")

        # 색상 정의
        bg_color = "white"
        header_bg = "#343a40"
        header_fg = "white"
        row_selected = "#3B8ED0"

        # Treeview 스타일
        style.configure("Treeview",
                        background=bg_color,
                        fieldbackground=bg_color,
                        foreground="black",
                        rowheight=35,
                        borderwidth=0,
                        font=("Malgun Gothic", 11))

        style.configure("Treeview.Heading",
                        background=header_bg,
                        foreground=header_fg,
                        relief="flat",
                        font=("Malgun Gothic", 11, "bold"))

        style.map("Treeview", background=[('selected', row_selected)], foreground=[('selected', 'white')])

        # 컬럼 정의
        columns = ("No", "Name", "Amount", "GuestOf", "Relation", "Affiliation", "Meal", "Note")
        self.tree = ttk.Treeview(self.list_frame, columns=columns, show="headings", style="Treeview")

        # 헤더 설정
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

        # --- [메인 리스트] 교차 채색 설정 ---
        self.tree.tag_configure("evenrow", background="#f8f9fa")  # 아주 연한 회색
        self.tree.tag_configure("oddrow", background="white")  # 흰색

        # 스크롤바
        self.scrollbar = ctk.CTkScrollbar(self.list_frame, orientation="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)

        self.tree.grid(row=1, column=0, sticky="nsew", padx=(20, 5), pady=(0, 20))
        self.scrollbar.grid(row=1, column=1, sticky="ns", padx=(0, 20), pady=(0, 20))

        # 테스트 데이터
        data = [
            (1, "홍길동", 100000, "신랑", "친구", "삼성전자 개발팀", 1, "축하합니다! 행복하세요."),
            (2, "김철수", 50000, "신부", "친척", "이모부", 2, ""),
            (3, "이영희", 300000, "신랑", "직장", "네이버", 1, "못가서 미안해"),
            (4, "박지민", 200000, "신부", "친구", "고등학교 동창", 1, ""),
            (5, "최민수", 50000, "신랑", "친척", "삼촌", 2, "잘 살아라"),
        ]

        for i, item in enumerate(data):
            formatted_values = list(item)
            formatted_values[2] = f"{item[2]:,}"

            # 짝수/홀수 판별하여 태그 적용
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=formatted_values, tags=(tag,))

    def create_bottom_dashboard(self):
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=20)
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid_columnconfigure(1, weight=1)

        # 왼쪽: 상세 분류
        self.stats_detail_frame = ctk.CTkFrame(self.bottom_frame, corner_radius=15, border_width=1, border_color="#ddd")
        self.stats_detail_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(self.stats_detail_frame, text="그룹별 상세 통계", font=("Malgun Gothic", 14, "bold")).pack(pady=10)

        # 미니 트리뷰
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

        # 데이터 리스트
        mini_data = [
            ("신랑측", "3명", "450,000 ", "4"),
            ("신부측", "2명", "250,000 ", "3")
        ]

        # 반복문을 통해 태그 적용
        for i, item in enumerate(mini_data):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.mini_tree.insert("", "end", values=item, tags=(tag,))

        # 오른쪽: 요약 카드
        self.summary_frame = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        self.summary_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        self.summary_frame.grid_columnconfigure(0, weight=1)
        self.summary_frame.grid_columnconfigure(1, weight=1)
        self.summary_frame.grid_rowconfigure(0, weight=1)
        self.summary_frame.grid_rowconfigure(1, weight=1)

        def create_card(parent, row, col, title, value, icon_color):
            card = ctk.CTkFrame(parent, corner_radius=15, fg_color=("white", "#333333"), border_width=2,
                                border_color="#eee")
            card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

            bar = ctk.CTkFrame(card, width=5, fg_color=icon_color, corner_radius=0)
            bar.pack(side="left", fill="y", padx=(0, 10))

            content = ctk.CTkFrame(card, fg_color="transparent")
            content.pack(side="left", fill="both", expand=True, pady=10)

            ctk.CTkLabel(content, text=title, font=("Malgun Gothic", 12), text_color="gray").pack(anchor="w")
            ctk.CTkLabel(content, text=value, font=("Roboto Medium", 20), text_color="black").pack(anchor="w")

        create_card(self.summary_frame, 0, 0, "전체 인원", "5 명", "#3B8ED0")
        create_card(self.summary_frame, 0, 1, "전체 식권", "7 장", "#2CC985")

        total_card = ctk.CTkFrame(self.summary_frame, corner_radius=15, fg_color="#E3F2FD", border_width=0)
        total_card.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(total_card, text="총 정산 금액", font=("Malgun Gothic", 14, "bold"), text_color="#1565C0").pack(
            side="left", padx=20)
        ctk.CTkLabel(total_card, text="700,000 원", font=("Roboto", 28, "bold"), text_color="#0D47A1").pack(side="right",
                                                                                                           padx=20)


if __name__ == "__main__":
    app = WeddingApp()
    app.mainloop()