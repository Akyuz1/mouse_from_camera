import cv2
import mediapipe as mp
import pyautogui
import math
import time
from collections import deque
import threading
import keyboard
import webbrowser
import shutil
import os
import json
import ctypes
from ctypes import wintypes

if hasattr(wintypes, "ULONG_PTR"):
    ULONG_PTR = wintypes.ULONG_PTR
else:
    ULONG_PTR = ctypes.c_uint64 if ctypes.sizeof(ctypes.c_void_p) == 8 else ctypes.c_uint32

user32 = ctypes.windll.user32

INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_WHEEL = 0x0800

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]

class INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD),
                ("mi", MOUSEINPUT)]

def win_move_rel(dx, dy):
    inp = INPUT(INPUT_MOUSE, MOUSEINPUT(int(dx), int(dy), 0, MOUSEEVENTF_MOVE, 0, 0))
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

pyautogui.FAILSAFE = False

# Kamera
cam_num = 0
kamera = cv2.VideoCapture(cam_num)

# Ekran boyutu
ekran_w, ekran_h = pyautogui.size()

# Mediapipe
mp_eller = mp.solutions.hands
eller = mp_eller.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=0,
    min_detection_confidence=0.1,
    min_tracking_confidence=0.5
)
cizici = mp.solutions.drawing_utils

# Ayarlar
base_deadzone = 30
fps = 30
frame_time = 1 / fps

# Click state
sol_basilimi = False
sag_basilimi = False

# Shared state
hedef_x, hedef_y = ekran_w // 2, ekran_h // 2
lock = threading.Lock()
running = True

# ================== MOUSE THREAD ==================
def mouse_move():
    global hedef_x, hedef_y, running, fps, base_deadzone, cam_num, frame_time

    control_panel = False
    options_reload = False

    onceki_x, onceki_y = ekran_w // 2, ekran_h // 2
    onceki_zaman = time.time()

    buffer_size = 45
    buf_x = deque(maxlen=buffer_size)
    buf_y = deque(maxlen=buffer_size)

    min_smooth = 0.1
    max_smooth = 6.0
    max_speed = 60
    max_frame_move = 12

    while running:

        if keyboard.is_pressed('ctrl+shift+"'):
            if control_panel == False:
                control_panel = True
                print("control panel is opening")
                dosya_yolu = os.path.abspath("ControlPanel.html")
                webbrowser.open(f"file:///{dosya_yolu}")
        else:
            control_panel = False

        if keyboard.is_pressed('ctrl+shift+r'):
            if not options_reload:
                options_reload = True
                try:
                    yeni_dosya = os.path.expanduser("~/Downloads/options_save.json")
                    if os.path.exists(yeni_dosya):
                        eski_dosya = os.path.join(os.getcwd(), "options_save.json")
                        if os.path.exists(eski_dosya):
                            os.remove(eski_dosya)

                        shutil.move(yeni_dosya, eski_dosya)
                        print("Ayar dosyası güncellendi.")

                        with open(eski_dosya, "r", encoding="utf-8") as f:
                            new_options = json.load(f)

                        max_speed = new_options["max_speed_"]
                        max_frame_move = new_options["max_frame_move_"]
                        min_smooth = new_options["min_smooth_"]
                        max_smooth = new_options["max_smooth_"]
                        fps = new_options["cam_fps_"]
                        cam_num = new_options["cam_num_"]
                        buffer_size = new_options["buffer_size_"]
                        base_deadzone = new_options["base_deadzone_"]

                        # fps değişince frame_time güncelle
                        frame_time = 1 / fps

                        # buffer değişince deque'leri yenile
                        buf_x = deque(buf_x, maxlen=buffer_size)
                        buf_y = deque(buf_y, maxlen=buffer_size)

                        print("Ayarlar başarıyla yüklendi.")
                        print(new_options)

                    else:
                        print("Uyarı: İndirilenlerde ayar dosyası bulunamadı.")
                except Exception as e:
                    print("Hata: Ayar değiştirme başarısız.")
                    print(e)
        else:
            options_reload = False
        
        smoothed_tx, smoothed_ty = pyautogui.position()
        with lock:
            tx, ty = int(hedef_x-100), int(hedef_y-200)
        simdiki_x, simdiki_y = pyautogui.position()
        dx = tx - simdiki_x
        dy = ty - simdiki_y
        mesafe = math.hypot(dx, dy)
        if mesafe < base_deadzone:
            continue
        
        hiz = min(mesafe / max(1/ fps, 0.001), max_frame_move)
        hiz_orani = hiz / max_frame_move
        smooth = max_smooth - (max_smooth - min_smooth) * hiz_orani

        smoothed_tx += dx * smooth
        smoothed_ty += dy * smooth

        # --- Relative move ---
        dx_rel = smoothed_tx - simdiki_x
        dy_rel = smoothed_ty - simdiki_y

        # Max speed clamp
        dx_rel = max(-max_frame_move, min(max_frame_move, dx_rel))
        dy_rel = max(-max_frame_move, min(max_frame_move, dy_rel))

        print(dy_rel)

        win_move_rel(dx_rel, dy_rel)


Thread = threading.Thread(target=mouse_move, daemon=True)
Thread.start()

# ================== CAMERA LOOP ==================
while True:
    baslangic = time.time()

    ok, kare = kamera.read()
    if not ok:
        continue

    kare = cv2.flip(kare, 1)
    h, w, _ = kare.shape

    rgb = cv2.cvtColor(kare, cv2.COLOR_BGR2RGB)
    sonuc = eller.process(rgb)

    if sonuc.multi_hand_landmarks and sonuc.multi_handedness:
        el = sonuc.multi_hand_landmarks[0]
        el_tipi = sonuc.multi_handedness[0].classification[0].label

        if el_tipi == "Right":
            lm = el.landmark

            # --- NON-LINEAR MAPPING ---
            with lock:
                hedef_x = lm[9].x * ekran_w * (0.05 - 0.2 + lm[9].x * 1.3)
                hedef_y = lm[9].y * ekran_h * (0.05 - 0.2 + lm[9].y * 1.6)

            # ---- TIKLAMALAR ----
            uy, dy = lm[8].y * h, lm[5].y * h
            sux, oux, yux = lm[20].x * w, lm[12].x * w, lm[16].x * w

            if abs(dy - uy) < 65 and abs(yux - oux) > 30:
                if not sol_basilimi:
                    pyautogui.mouseDown(button="left")
                    sol_basilimi = True
            else:
                if sol_basilimi:
                    pyautogui.mouseUp(button="left")
                    sol_basilimi = False

            ouy, ody = lm[12].y * h, lm[9].y * h

            if abs(ody - ouy) < 65:
                if not sag_basilimi:
                    pyautogui.mouseDown(button="right")
                    sag_basilimi = True
            else:
                if sag_basilimi:
                    pyautogui.mouseUp(button="right")
                    sag_basilimi = False

            iux, idx = lm[8].x * w, lm[5].x * w
            if abs(sux - yux) < 30 and abs(yux - oux) < 30:
                pyautogui.scroll(int(((lm[4].y * h) - (lm[8].y*h))*0.4)-50)
                
            cizici.draw_landmarks(kare, el, mp_eller.HAND_CONNECTIONS)

    cv2.imshow("Mouse From Camera", kare)

    if keyboard.is_pressed("esc"):
        running = False
        break

    gecen = time.time() - baslangic
    if gecen < frame_time:
        time.sleep(frame_time - gecen)

kamera.release()
cv2.destroyAllWindows()
