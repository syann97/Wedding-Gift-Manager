import customtkinter as ctk
import webbrowser  # 웹사이트 열기 위한 모듈


class AboutDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("프로그램 정보")
        self.geometry("320x350")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self._init_ui()
        self._center_window(parent)

    def _init_ui(self):
        # 전체 컨테이너
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # 1. 프로그램 제목 (크게)
        ctk.CTkLabel(frame, text="누나를 위한 축의금 정산 매니저 Pro",
                     font=("Malgun Gothic", 18, "bold"), text_color="#1E88E5").pack(pady=(20, 5))

        # 2. 버전 정보
        ctk.CTkLabel(frame, text="Version 1.0.0",
                     font=("Roboto", 12), text_color="gray").pack(pady=(0, 20))

        # 구분선
        ctk.CTkFrame(frame, height=2, fg_color="#ddd").pack(fill="x", padx=40, pady=10)

        # 3. 개발자 정보
        ctk.CTkLabel(frame, text="Developed by",
                     font=("Malgun Gothic", 12)).pack(pady=(10, 0))

        ctk.CTkLabel(frame, text="Seyoung (Developer)",
                     font=("Roboto", 14, "bold")).pack(pady=(0, 10))

        # 4. 깃허브 링크
        self.github_url = "https://github.com/syann97"

        self.lbl_link = ctk.CTkLabel(frame, text="Visit GitHub Profile ↗",
                                     font=("Roboto", 12, "underline"),
                                     text_color="#1E88E5", cursor="hand2")
        self.lbl_link.pack(pady=5)

        # 클릭 이벤트 연결
        self.lbl_link.bind("<Button-1>", lambda e: webbrowser.open_new(self.github_url))

        # 5. 닫기 버튼
        ctk.CTkButton(frame, text="닫기", width=100, command=self.destroy).pack(side="bottom", pady=10)

    def _center_window(self, parent):
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (400 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (300 // 2)
        self.geometry(f"+{x}+{y}")