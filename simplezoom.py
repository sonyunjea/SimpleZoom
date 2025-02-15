import tkinter as tk
from tkinter import ttk
from pyautogui import position
from PIL import Image, ImageTk, ImageGrab

class SimpleZoom(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SimpleZoom - 화면 확대 프로그램")
        self.geometry("400x300")
        self.ratio = 4  # 2배 확대
        self.new_image = None
        self.fixed_region = (1650, 810, 1919, 1079)  # 고정된 영역 좌표
        self.init_ui()
        self.update_zoom()

    def init_ui(self):
        self.state_label = tk.Label(self, text="X2.0 | Fixed Position")
        self.state_label.pack()
        
        self.label_img = tk.Label(self, image=None)
        self.label_img.pack()

        self.bind('<Key>', self.key_pressed)
        self.bind('<MouseWheel>', self.mouse_wheel)
        self.bind('<Button-4>', self.mouse_wheel)
        self.bind('<Button-5>', self.mouse_wheel)
        
        self.transparency_slider = ttk.Scale(self, from_=0.1, to=1.0, 
                                             orient='horizontal', command=self.set_transparency)
        self.transparency_slider.set(1.0)
        self.transparency_slider.pack()
        
    def update_zoom(self):
        self.state_label.config(text=f'X{self.ratio} | Fixed Position')

        ss_img = ImageGrab.grab(self.fixed_region)
        resized_image = ss_img.resize((round((self.fixed_region[2] - self.fixed_region[0]) * self.ratio),
                                       round((self.fixed_region[3] - self.fixed_region[1]) * self.ratio)), Image.LANCZOS)
        
        self.new_image = ImageTk.PhotoImage(resized_image)
        self.label_img.config(image=self.new_image)
        
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
