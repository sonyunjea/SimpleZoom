import tkinter as tk
from tkinter import ttk
from pyautogui import position  # 마우스 좌표 가져오는 함수
from PIL import Image, ImageTk, ImageGrab

class SimpleZoom(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SimpleZoom - 화면 확대 프로그램")

        # ─── 해상도 관련 멤버 변수 ───────────────────────────
        # 기본 해상도(돋보기 렌즈 크기)
        self.win_width = 1200
        self.win_height = 800
        # 팝업 창 참조를 보관할 변수 (중복 생성 방지용)
        self.res_window = None
        # 해상도 목록 (리스트로 관리)
        self.res_options = [
            "1920x1080",
            "1680x1050",
            "1600x1024",
            "1600x900",
            "1440x1080",
            "1440x900",
            "1400x1050",
            "1366x768",
            "1280x1024",
            "1280x960",
            "1280x800",
            "1280x720",
            "1152x864"
        ]
        # ─────────────────────────────────────────────────────

        # 처음 창 크기를 기본 해상도로 세팅
        self.geometry(f"{self.win_width}x{self.win_height}")
        self.resizable(False, False)

        self.ratio = 4  # 확대 배율 기본값
        # 사용자 지정 캡처 좌표 초기값
        self.x = 0
        self.y = 0

        # UI 구성 & 업데이트 루프 시작
        self.init_ui()
        self.update_zoom()

    def init_ui(self):
        # ─── 해상도 선택 버튼 ─────────────────────────────────
        res_frame = tk.Frame(self)
        res_frame.pack(fill='x', padx=10, pady=5)

        # 보물 상자 뚜껑: “해상도 선택” 버튼
        self.res_button = tk.Button(
            res_frame,
            text="해상도 선택",
            command=self.open_res_selection  # 버튼 클릭 시 팝업 열기
        )
        self.res_button.pack(side='left')
        # ─────────────────────────────────────────────────────

        # ─── 캡처 좌표 입력창 (X, Y) ─────────────────────────
        coord_frame = tk.Frame(self)
        coord_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(coord_frame, text="X 좌표:").pack(side='left')
        self.x_entry = tk.Entry(coord_frame, width=6)
        self.x_entry.insert(0, str(self.x))
        self.x_entry.pack(side='left', padx=(0, 15))

        tk.Label(coord_frame, text="Y 좌표:").pack(side='left')
        self.y_entry = tk.Entry(coord_frame, width=6)
        self.y_entry.insert(0, str(self.y))
        self.y_entry.pack(side='left', padx=(0, 15))
        # ─────────────────────────────────────────────────────

        # ─── 상태 라벨 (배율 및 사용자 지정 좌표) ────────────────
        self.state_label = tk.Label(
            self,
            text=f"배율 X{self.ratio:.1f} | 위치 ({self.x}, {self.y})"
        )
        self.state_label.pack()

        # ─── 마우스 위치 레이블 (실시간 업데이트) ──────────────
        self.mouse_label = tk.Label(self, text="마우스 위치: (?, ?)")
        self.mouse_label.pack()
        # ─────────────────────────────────────────────────────

        # ─── 확대된 이미지를 표시할 레이블 ────────────────────
        self.label_img = tk.Label(self)
        self.label_img.pack()
        # ─────────────────────────────────────────────────────

        # 키 입력(ESC) 및 마우스 휠 바인딩
        self.bind('<Key>', self.key_pressed)
        self.bind('<MouseWheel>', self.mouse_wheel)
        self.bind('<Button-4>', self.mouse_wheel)
        self.bind('<Button-5>', self.mouse_wheel)

        # ─── 투명도 슬라이더 ──────────────────────────────────
        self.transparency_slider = ttk.Scale(
            self, from_=0.1, to=1.0,
            orient='horizontal',
            command=self.set_transparency
        )
        self.transparency_slider.set(1.0)
        self.transparency_slider.pack(pady=5)
        # ─────────────────────────────────────────────────────

    def open_res_selection(self):
        """
        '해상도 선택' 버튼을 누르면 호출됩니다.
        - 이미 팝업이 떠 있으면(Popup Window가 존재하면) 그냥 포커스만 가져오고,
        - 없으면 새 Toplevel을 생성해서 해상도 Listbox를 띄웁니다.
        """
        # 팝업 창이 이미 있으면 포커스만 올리고 리턴
        if self.res_window is not None and self.res_window.winfo_exists():
            self.res_window.lift()
            return

        # 새로운 팝업(Toplevel) 생성
        self.res_window = tk.Toplevel(self)
        self.res_window.title("해상도 선택")
        # 팝업 크기와 위치는 간단히 기본값으로 두거나, 원하면 self 위치 근처에 띄울 수 있습니다
        self.res_window.geometry("200x300")  # 예시 크기 (너비x높이)
        self.res_window.resizable(False, False)

        # Listbox + Scrollbar 배치
        scrollbar = tk.Scrollbar(self.res_window)
        scrollbar.pack(side='right', fill='y')

        self.res_listbox = tk.Listbox(
            self.res_window,
            yscrollcommand=scrollbar.set,
            selectmode='single'
        )
        # 해상도 목록을 Listbox에 추가
        for res in self.res_options:
            self.res_listbox.insert(tk.END, res)
        self.res_listbox.pack(side='left', fill='both', expand=True)

        scrollbar.config(command=self.res_listbox.yview)

        # 더블클릭(<<Double-Button-1>>) 혹은 <Return> 키로 선택하면 해상도 변경
        self.res_listbox.bind(
            "<Double-Button-1>",
            lambda event: self.select_resolution()
        )
        # 엔터키로도 선택 가능
        self.res_listbox.bind(
            "<Return>",
            lambda event: self.select_resolution()
        )

    def select_resolution(self):
        """
        팝업 Listbox에서 해상도를 더블클릭하거나
        엔터를 누르면 호출됩니다.
        - 선택된 문자열을 파싱해서 self.win_width, self.win_height 업데이트
        - 팝업 창을 닫고, 메인 창 크기를 새 해상도로 변경
        """
        # Listbox에서 선택된 인덱스 가져오기
        sel = self.res_listbox.curselection()
        if not sel:
            return  # 아무것도 선택되지 않았으면 리턴

        idx = sel[0]
        res_str = self.res_listbox.get(idx)  # 예: "1920x1080"
        try:
            w_str, h_str = res_str.split('x')
            new_w = int(w_str)
            new_h = int(h_str)
        except ValueError:
            # 파싱 실패 시 기본 해상도로 복귀
            new_w, new_h = 1200, 800

        # 멤버 변수 업데이트
        self.win_width = new_w
        self.win_height = new_h
        # 메인 창 크기 변경
        self.geometry(f"{self.win_width}x{self.win_height}")

        # 팝업 창 닫기
        if self.res_window and self.res_window.winfo_exists():
            self.res_window.destroy()
            self.res_window = None

    def update_zoom(self):
        # ─── 1) 사용자 입력 좌표 읽기 ───────────────────────────
        try:
            x_val = int(self.x_entry.get())
            y_val = int(self.y_entry.get())
        except ValueError:
            x_val = 0
            y_val = 0

        if x_val < 0:
            x_val = 0
        if y_val < 0:
            y_val = 0

        self.x, self.y = x_val, y_val

        # ─── 2) 상태 라벨 업데이트 ───────────────────────────
        self.state_label.config(
            text=f"배율 X{self.ratio:.1f} | 위치 ({self.x}, {self.y})"
        )

        # ─── 3) 마우스 위치 가져와서 레이블 갱신 ───────────────
        mx, my = position()
        self.mouse_label.config(text=f"마우스 위치: ({mx}, {my})")

        # ─── 4) 캡처할 원본 영역 크기 계산 ────────────────────
        # 사용자가 선택한 해상도(렌즈 크기) ÷ 배율 = 원본 캡처 크기
        crop_width = int(self.win_width / self.ratio)
        crop_height = int(self.win_height / self.ratio)

        # 화면 해상도 얻어서 영역이 화면 밖으로 나가지 않도록 보정
        screen_w, screen_h = ImageGrab.grab().size
        if self.x + crop_width > screen_w:
            self.x = max(0, screen_w - crop_width)
        if self.y + crop_height > screen_h:
            self.y = max(0, screen_h - crop_height)

        region = (self.x, self.y, self.x + crop_width, self.y + crop_height)
        ss_img = ImageGrab.grab(region)

        # ─── 5) 캡처된 이미지를 선택된 해상도로 리사이즈 ────────
        resized_image = ss_img.resize((self.win_width, self.win_height), Image.LANCZOS)
        self.new_image = ImageTk.PhotoImage(resized_image)
        self.label_img.config(image=self.new_image)

        # ─── 6) 0.1초 뒤에 다시 업데이트 ─────────────────────
        self.after(100, self.update_zoom)

    def key_pressed(self, event):
        if event.keysym == "Escape":
            self.destroy()

    def mouse_wheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.ratio = max(1.0, round(self.ratio - 0.1, 2))
        elif event.num == 4 or event.delta == 120:
            self.ratio = round(self.ratio + 0.1, 2)

    def set_transparency(self, value):
        self.attributes('-alpha', float(value))


if __name__ == "__main__":
    app = SimpleZoom()
    app.mainloop()
