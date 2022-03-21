import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from licenta import LSB_encode, LSB_decode
from crypto_functions import OFB_decrypt, OFB_encrypt
import zlib

global carrier_text, plaintext_text 

#add these later to GUI settings
iv_delimiter = "8058060923" 
ct_delimiter = "6320986309" 
key = "abcdefghabcdefgh"

# create the root window
root = tk.Tk()
root.title('Steganography App')
root.resizable(True, True)
root.geometry('550x230')
root.configure(background="lightgrey")

rows = 0
while rows < 50:
    root.rowconfigure(rows, weight=1)
    root.columnconfigure(rows,weight=1)
    rows += 1


#variables + textboxes
carrier_text = StringVar(value = "No carrier selected")
plaintext_text = StringVar(value = "No plaintext selected")
embedded_text = StringVar(value = "No encoded file selected")
carrier_tb = tk.Label(root, textvariable=carrier_text)
plaintext_tb = tk.Label(root, textvariable=plaintext_text)
embedded_tb = tk.Label(root, textvariable=embedded_text)

def select_carrier():
    global carrier_text
    filetypes = (
        ('Audio Files', '*.wav'),
    )

    filename = fd.askopenfilename(
        title='Select carrier file',
        initialdir='/',
        filetypes=filetypes)
    carrier_text.set(filename)


def select_plaintext():
    global plaintext_text
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Select carrier file',
        initialdir='/',
        filetypes=filetypes)
    plaintext_text.set(filename)


def select_encoded_file():
    global embedded_text
    filetypes = (
        ('Audio Files', '*.wav'),
    )

    filename = fd.askopenfilename(
        title='Select encoded file',
        initialdir='/',
        filetypes=filetypes)
    embedded_text.set(filename)


def encode():
    #add these variables to the GUI later
    embedded_audio_path = "Resources/audio_file_embedded.wav"
    offset = 2

    #getting audio + plaintext files paths
    carrier_path = str(carrier_tb.cget("text"))
    plaintext_path = str(plaintext_tb.cget("text"))

    reader = open(plaintext_path, "r", encoding="utf-8")
    plaintext = reader.read()
    compressed_text = zlib.compress(bytes(plaintext, 'utf-8'))
    ofb_result = OFB_encrypt(compressed_text, key)
    LSB_encode(ofb_result[0], ofb_result[1], carrier_path, embedded_audio_path, offset, iv_delimiter, ct_delimiter)
    reader.close()

def decode():
    #add these variables to the GUI later
    recoveredtext_path = "Resources/decrypted.txt"
    embedded_audio_path = str(embedded_tb.cget("text"))
    offset = 2
    decoded = LSB_decode(embedded_audio_path, offset, iv_delimiter, ct_delimiter)
    text = OFB_decrypt(decoded, "abcdefghabcdefgh")
    decompressed_text = zlib.decompress(text)

    writer = open(recoveredtext_path, "w", encoding="utf-8")
    writer.write(str(decompressed_text, 'utf-8'))
    writer.close()

# open button
open_button = ttk.Button(root, text='Select carrier file', command = select_carrier)
open_button2 = ttk.Button(root, text = 'Select plaintext', command = select_plaintext)
encode_button = ttk.Button(root, text = 'Start encoding', command = encode)
open_button3 = ttk.Button(root, text = 'Select encoded file', command = select_encoded_file)
decode_button = ttk.Button(root, text = 'Start decoding', command = decode)
encoded_button = ttk.Button(root, text = 'Select encoded file', command = select_encoded_file)

carrier_tb.grid(row = 2, column = 2, sticky = "nw")
open_button.grid(row = 2, column = 45, sticky = "ne")
plaintext_tb.grid(row = 3, column = 2, sticky = "nw")
open_button2.grid(row = 3, column = 45, sticky = "ne")
embedded_tb.grid(row = 4, column = 2, sticky = "nw")
encoded_button.grid(row = 4, column = 45, sticky = "ne")
encode_button.grid(row = 7, column = 45, sticky = "ne")
decode_button.grid(row = 8, column = 45, sticky = "ne")

# run the application
root.mainloop()