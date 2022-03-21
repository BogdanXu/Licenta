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

# create the root window
root = tk.Tk()
root.title('Steganography App')
root.resizable(True, True)
root.geometry('720x250')
root.configure(background="lightgrey")

rows = 0
while rows < 50:
    root.rowconfigure(rows, weight=1)
    root.columnconfigure(rows,weight=1)
    rows += 1


#variables + textboxes
encode_box = tk.Label(root)
decode_box = tk.Label(root)
encoding_label = tk.Label(encode_box, text = "Encoding a file with a secret message")
decoding_label = tk.Label(decode_box, text = "Decoding a secret message from a file")
key_label = tk.Label(root, text = "Write the 16 bytes key used for encoding/decoding", wraplength=200)
carrier_text = StringVar(value = "Step 1:")
plaintext_text = StringVar(value = "Step 2: ")
embedded_text = StringVar(value = "Step 1: ")
carrier_tb = tk.Label(encode_box, textvariable=carrier_text, width=30, wraplength=200, height=2)
plaintext_tb = tk.Label(encode_box, textvariable=plaintext_text, width=30, wraplength=200, height=2)
embedded_tb = tk.Label(decode_box, textvariable=embedded_text, width=30, wraplength=200, height=2)
offset_label = tk.Label(root, text = "Enter the offset between the encoded bits")
key_tb = tk.Text(root, height = 1, width = 20)
key_tb.insert(1.0, "sixteenbyteskeyy")
offset_tb = tk.Text(root, height = 1, width = 20)
offset_tb.insert(1.0, "2")




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

def get_key():
    key = key_tb.get("1.0", "end-1c")
    return key

def get_offset():
    offset = offset_tb.get("1.0", "end-1c")
    return int(offset)

def encode():
    #add these variables to the GUI later
    embedded_audio_path = "Resources/audio_file_embedded.wav"
    offset = get_offset()

    #getting audio + plaintext files paths
    carrier_path = str(carrier_tb.cget("text"))
    plaintext_path = str(plaintext_tb.cget("text"))

    reader = open(plaintext_path, "r", encoding="utf-8")
    plaintext = reader.read()
    compressed_text = zlib.compress(bytes(plaintext, 'utf-8'))
    key = get_key()
    print("Key used is: %s" % key)
    ofb_result = OFB_encrypt(compressed_text, key)
    LSB_encode(ofb_result[0], ofb_result[1], carrier_path, embedded_audio_path, offset, iv_delimiter, ct_delimiter)
    reader.close()

def decode():
    #add these variables to the GUI later
    recoveredtext_path = "Resources/decrypted.txt"
    embedded_audio_path = str(embedded_tb.cget("text"))
    offset = get_offset()
    decoded = LSB_decode(embedded_audio_path, offset, iv_delimiter, ct_delimiter)
    key = get_key()
    print("Key used is: %s" % key)
    text = OFB_decrypt(decoded, key)
    decompressed_text = zlib.decompress(text)

    writer = open(recoveredtext_path, "w", encoding="utf-8")
    writer.write(str(decompressed_text, 'utf-8'))
    writer.close()

# open button
open_button = ttk.Button(encode_box, text='Select carrier file', command = select_carrier)
open_button2 = ttk.Button(encode_box, text = 'Select plaintext', command = select_plaintext)
encode_button = ttk.Button(root, text = 'Start encoding', command = encode)
decode_button = ttk.Button(root, text = 'Start decoding', command = decode)
encoded_button = ttk.Button(decode_box, text = 'Select encoded file', command = select_encoded_file)


# encoding_label.grid(row = 1, column = 5, sticky = "nw")
# decoding_label.grid(row = 1, column = 35, sticky = "ne")
# carrier_tb.grid(row = 2, column = 2, sticky = "nw")
# open_button.grid(row = 2, column = 10, sticky = "ne")
# plaintext_tb.grid(row = 3, column = 2, sticky = "nw")
# open_button2.grid(row = 3, column = 10, sticky = "ne")
# embedded_tb.grid(row = 2, column = 25, sticky = "nw")
# encoded_button.grid(row = 2, column = 45, sticky = "ne")
# key_tb.grid(row = 5, column = 15, sticky = "nesw")
# encode_button.grid(row = 6, column = 15, sticky = "nesw")
# decode_button.grid(row = 7, column = 15, sticky = "nesw")

encode_box.pack(ipadx=10, ipady=10, expand=False, fill='both', side = 'left')


decode_box.pack(ipadx=10, ipady=10, expand=False, fill='both', side = 'right')


encoding_label.pack(pady=5)
decoding_label.pack(pady=5)
carrier_tb.pack(pady=3)
open_button.pack()
plaintext_tb.pack()
open_button2.pack()
embedded_tb.pack(pady=2)
encoded_button.pack()
key_label.pack(pady=5)
key_tb.pack(pady=2)
offset_label.pack(pady=5)
offset_tb.pack(pady=2)
encode_button.pack(padx=5,pady=10)
decode_button.pack(pady=0)



# run the application
root.mainloop()