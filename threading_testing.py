import threading
import tkinter as tk
import time

class App:
    def __init__(self, parent):
        self.button = tk.Button(parent, text='init', command=self.begin)
        self.button.pack()
    def func(self):
        '''long-running work'''
        self.button.config(text='func')
        time.sleep(1)
        self.button.config(text='continue')
        time.sleep(1)
        self.button.config(text='done')
        self.button.config(state=tk.NORMAL)
    def begin(self):
        '''start a thread and connect it to func'''
        self.button.config(state=tk.DISABLED)
        threading.Thread(target=self.func, daemon=True).start()

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()