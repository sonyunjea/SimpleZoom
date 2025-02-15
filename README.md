# **SimpleZoom - Screen Magnification Program**

## **📌 Introduction**
SimpleZoom is a lightweight screen magnification program that enlarges a specific region of the screen by 2x.
It captures a fixed coordinate area in real-time, magnifies it, and provides transparency control.

---

## **📜 Key Features**
✅ **2x magnification feature**  
✅ **Fixed coordinate magnification (x: 1650, y: 810 → x: 1919, y: 1079)**  
✅ **Real-time magnification updates (every 100ms)**  
✅ **Adjustable transparency**  
✅ **Exit program with the ESC key**  
✅ **Zoom in/out using the mouse wheel**  

---

## **💻 How to Use**
### **1️⃣ Running the Program**
To run SimpleZoom in a Python-installed environment, enter the following command:
```sh
python simplezoom.py
```

### **2️⃣ Shortcut Keys**
| Shortcut Key    | Description |
|----------------|----------------|
| `ESC` Key | Exit the program |
| `Mouse Wheel Up` | Increase magnification (+0.1) |
| `Mouse Wheel Down` | Decrease magnification (-0.1) |
| `Transparency Slider` | Adjust transparency of the magnified screen |

---

## **📦 Required Packages**
The following packages are required. If they are not installed, please install them before running the program.

```sh
pip install pillow pyautogui
```

---

## **🔧 Changing Settings**
By default, the magnification area is set to **(x: 1650, y: 810, x: 1919, y: 1079)**.  
If you want to use different coordinates, modify the **`self.fixed_region` value** in the `simplezoom.py` file.

```python
self.fixed_region = (NEW_X1, NEW_Y1, NEW_X2, NEW_Y2)
```

---

## **📌 Notes**
- This program has been tested only on Windows.
- It uses the `pyautogui` and `Pillow` libraries to capture and magnify the screen.
- Adjustments may be required for multi-monitor environments.

---

## **📜 License**
This project is freely available for use and modification as needed. 🚀

---

![심플줌예시](https://github.com/user-attachments/assets/5095ac36-fce3-411c-b033-c7564632cbf6)


Run **SimpleZoom** now and easily magnify your screen! 🔍😊

