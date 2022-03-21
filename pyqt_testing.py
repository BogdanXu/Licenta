import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from licenta import LSB_encode, LSB_decode
from crypto_functions import OFB_decrypt, OFB_encrypt