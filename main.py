import tkinter as tk
from tkinter import ttk
from time import sleep
import time
import threading
import keyboard
import pyautogui
import os
import subprocess
from tkinter import filedialog
from tkinter import messagebox
from threading import Thread
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


def set_timer(time):
    sleep(time)


def image_procc():
    img = cv.imread('start3.PNG')
    assert img is not None, "file could not be read, check with os.path.exists()"
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=1)
    #  cv.imshow("result",opening) resmin son hali
    return opening


def open_program(game_path):
    try:
        subprocess.Popen(game_path)
        time_thread = Thread(target=set_timer(5))
        time_thread.start()
        time_thread.join()
        locationbutton = pyautogui.locateOnScreen(image_procc(), confidence=.7)  # confidence tolerans oluyor eşleşmeye
        # yakınlık değeri bu
        pyautogui.click(locationbutton)
        time_thread2 = Thread(target=set_timer(45))
        time_thread2.start()
        time_thread2.join()
    except Exception as ex:
        messagebox.showerror("Hata", f"Oyun başlatılamadı: {str(ex)}")


class App:
    def __init__(self, master):
        self.master = master
        self.is_running = False

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both')

        # create tab 2 and widgets inside it
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text='Tab 2')

        self.game_path_label = tk.Label(self.tab2, text="Oyun Yolu:")
        self.game_path_label.pack(side=tk.LEFT, padx=5)

        self.game_path_entry = tk.Entry(self.tab2)
        self.game_path_entry.pack(side=tk.LEFT, padx=5)

        self.game_path_button = tk.Button(self.tab2, text="Seç", command=self.select_game_path)
        self.game_path_button.pack(side=tk.LEFT, padx=5)

        self.start_game_button = tk.Button(self.tab2, text="Oyunu Başlat", command=self.start_game)
        self.start_game_button.pack(side=tk.LEFT, padx=5)

        self.username_label = tk.Label(self.tab2, text="Kullanıcı Adı:")
        self.username_label.pack(side=tk.LEFT, padx=5)

        self.username_entry = tk.Entry(self.tab2)
        self.username_entry.pack(side=tk.LEFT, padx=5)

        self.password_label = tk.Label(self.tab2, text="Şifre:")
        self.password_label.pack(side=tk.LEFT, padx=5)

        self.password_entry = tk.Entry(self.tab2, show="*")
        self.password_entry.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(self.tab2, text="Save", command=self.save_settings)
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.load_settings()  # kaydedilen ayarları yükle

    def save_settings(self):
        # kaydedilecek bilgileri dosyaya yaz
        game_path = self.game_path_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        with open('settings.txt', 'w') as f:
            f.write(f"{game_path}\n{username}\n{password}")

    def load_settings(self):
        # kaydedilen ayarları yükle
        try:
            with open('settings.txt', 'r') as f:
                game_path, username, password = f.read().splitlines()

            self.game_path_entry.insert(0, game_path)
            self.username_entry.insert(0, username)
            self.password_entry.insert(0, password)
        except FileNotFoundError:
            pass

    def select_game_path(self):
        game_path = filedialog.askopenfilename()
        self.game_path_entry.delete(0, tk.END)
        self.game_path_entry.insert(0, game_path)

    def start_game(self):
        game_path = self.game_path_entry.get()
        if game_path == "":
            messagebox.showwarning("Hata", "Lütfen oyun yolu seçin.")
            return

        try:
            image_procc()
            new_thread = Thread(target=open_program(game_path))
            new_thread.start()
            new_thread.join()
            # enter username and password
            pyautogui.typewrite(self.username_entry.get())
            keyboard.press('Tab')
            time.sleep(0.5)
            keyboard.release('Tab')
            time.sleep(0.5)
            pyautogui.typewrite(self.password_entry.get())
        except Exception as ex:
            messagebox.showerror("Hata", f"Oyun başlatılamadı: {str(ex)}")


root = tk.Tk()
root.configure(background="blue")
app = App(root)
root.mainloop()
