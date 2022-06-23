import base64
import tkinter as tk
from tkinter import StringVar, ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, showerror
from fft_decoder import fft_decoder
from fft_encoder import fft_encoder
from lsb_functions import LSB_encode, LSB_decode, get_folder_from_path
from crypto_functions import OFB_decrypt, OFB_encrypt

import threading
import converter

global carrier_text, plaintext_text 

iv_delimiter = "GE4" 
ct_delimiter = "0X3"
wav_subtypes = ["PCM_8", "PCM_16", "PCM_24", "PCM_32", "FLOAT", "DOUBLE"] 

# create the root window
root = tk.Tk()
root.title('Steganography App')
root.resizable(True, True)
root.geometry('720x300')
root.configure(background="lightgrey")

rows = 0
while rows < 50:
    root.rowconfigure(rows, weight=1)
    root.columnconfigure(rows,weight=1)
    rows += 1

#variables + textboxes
tab_control = ttk.Notebook(root)
dropdown_clicked = StringVar(root)
dropdown_clicked.set(wav_subtypes[0])
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text ='Steganography operations')
tab_control.add(tab2, text ='Settings')
tab_control.pack(expand = 1, fill = "both")
encode_box = ttk.Label(tab1)
decode_box = ttk.Label(tab1)
encoding_label = ttk.Label(encode_box, text = "Encoding a file with a secret message")
decoding_label = ttk.Label(decode_box, text = "Decoding a secret message from a file")
key_label = ttk.Label(tab1, text = "16 character key for AES encryption/decryption used in LSB mode", wraplength=200, justify="center")
carrier_text = StringVar(value = "Step 1: ")
plaintext_text = StringVar(value = "Step 2: ")
embedded_text = StringVar(value = "Step 1: ")
drop = ttk.OptionMenu(tab2, dropdown_clicked, wav_subtypes[0], *wav_subtypes)
carrier_tb = ttk.Label(encode_box, textvariable=carrier_text, width=30, wraplength=200)
plaintext_tb = ttk.Label(encode_box, textvariable=plaintext_text, width=30, wraplength=200)
embedded_tb = ttk.Label(decode_box, textvariable=embedded_text, width=30, wraplength=200)
offset_label = ttk.Label(tab2, text = "Offset between the encoded bits")
iv_del_label = ttk.Label(tab2, text = "First delimiter used to separate data")
ct_del_label = ttk.Label(tab2, text = "Second delimiter used to separate data")
key_tb = tk.Text(tab1, height = 1, width = 20)
iv_delimiter_tb = tk.Text(tab2, height = 1, width = 20)
ct_delimiter_tb = tk.Text(tab2, height = 1, width = 20)
key_tb.insert(1.0, "sixteenbyteskeyy")
offset_tb = tk.Text(tab2, height = 1, width = 20)
offset_tb.insert(1.0, "2")
iv_delimiter_tb.insert(1.0, iv_delimiter)
ct_delimiter_tb.insert(1.0, ct_delimiter)



def select_carrier():
    global carrier_text
    filetypes = (
        ('Audio Files', '*.wav'),
    )

    filename = fd.askopenfilename(
        title='Select carrier file',
        initialdir='/',
        filetypes=filetypes)
    if len(filename) == 0:
        showerror("No file selected", "Please select a .wav file for encoding")
    else:
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
    if len(filename) == 0:
        showerror("No file selected", "Please select any file for LSB encoding or a .txt file for FFT encoding")
    else:
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
    if len(filename) == 0:
        showerror("No file selected", "Please select a .wav file for decoding")
    else:
        embedded_text.set(filename)


def get_key():
    key = key_tb.get("1.0", "end-1c")
    return key

def get_offset():
    offset = offset_tb.get("1.0", "end-1c")
    return int(offset)


def get_iv_del():
    iv_del = iv_delimiter_tb.get("1.0", "end-1c")
    return iv_del


def get_ct_del():
    ct_del = ct_delimiter_tb.get("1.0", "end-1c")
    return ct_del


def encode():
    offset = get_offset()

    #getting audio + plaintext files paths
    carrier_path = str(carrier_tb.cget("text"))
    plaintext_path = str(plaintext_tb.cget("text"))

    if carrier_path == "Step 1: " or plaintext_path == "Step 2: ":
        showerror("No file selected","Please select both a 16-bit encoded .wav file and a file to be encoded" )
    elif offset == 0:
        showerror("Invalid offset","Offset must be at least 1" )
    else:
        embedded_audio_path = get_folder_from_path(carrier_path) + "/embedded_audio.wav"

        #b64encode read
        with open(plaintext_path, "rb") as stego_file:
            b64string = stego_file.read()
        compressed_text = b64string

        #encryption
        key = get_key()
        print("Key used is: %s" % key)
        ofb_result = OFB_encrypt(compressed_text, key)

        iv_delimiter = get_iv_del()
        ct_delimiter = get_ct_del()

        #encoding
        try:
            LSB_encode(ofb_result[0], ofb_result[1], carrier_path, embedded_audio_path, offset, iv_delimiter, ct_delimiter)
        except Exception:
            showerror(title = "Wrong .wav subtype", message = "The selected file is not a 16 bit PCM file. Try converting the file to PCM_16 in Settings.")
        stego_file.close()

    pb.stop()
    pb.pack_forget()


def start_fft_encoding_in_bg():
    pb.pack(pady=2)
    pb.start(10)
    thread = threading.Thread(target=fft_encode)
    thread.start()
    #thread.join()
    #pb.stop()

def start_fft_decoding_in_bg():
    pb.pack(pady=2)
    pb.start(10)
    thread2 = threading.Thread(target=fft_decode)
    thread2.start()

def start_lsb_encoding_in_bg():
    pb.pack(pady=2)
    pb.start(10)
    thread3 = threading.Thread(target=encode)
    thread3.start()

def start_lsb_decoding_in_bg():
    pb.pack(pady=2)
    pb.start(10)
    thread4 = threading.Thread(target=decode)
    thread4.start()

def decode():
    embedded_audio_path = str(embedded_tb.cget("text"))
    recoveredtext_path = get_folder_from_path(embedded_audio_path) + "/recovered.txt"

    offset = get_offset()
    iv_delimiter = get_iv_del()
    ct_delimiter = get_ct_del()

    #decoding
    decoded = LSB_decode(embedded_audio_path, offset, iv_delimiter, ct_delimiter)

    #decryption
    key = get_key()
    print("Key used is: %s" % key)
    text = OFB_decrypt(decoded, key)

    #decompression
    #decompressed_text = zlib.decompress(text)
    decompressed_text = text

    #b64decode
    writer = open(recoveredtext_path, "wb")
    writer.write(decompressed_text)
    writer.close()
    pb.stop()
    pb.pack_forget()

def fft_encode():
    carrier_path = str(carrier_tb.cget("text"))
    plaintext_path = str(plaintext_tb.cget("text"))

    if carrier_path == "Step 1: " or plaintext_path == "Step 2: ":
        showerror("No file selected","Please select both a 16-bit encoded .wav file and a file to be encoded" )
    else:
        reader = open(plaintext_path, "r", encoding="utf-8")
        stego_message = reader.read()
        fft_encoder(carrier_path, stego_message)
    
    pb.stop()
    pb.pack_forget()


def fft_decode():
    embedded_audio_path = str(embedded_tb.cget("text"))
    if embedded_audio_path == "Step 1: ":
        showerror("No file selected", "Please select a .wav file to be decoded")
    else:
        try:
            fft_decoder(embedded_audio_path)
        except Exception:
            showerror(title = "Wrong .wav subtype", message = "The selected file is of a wrong subtype. For applying FFT encoding and decoding to a .wav file, convert the file you want to encode on to FLOAT in Settings.")
    pb.stop()
    pb.pack_forget()
    
def subtype_convert():
    carrier_path = str(carrier_tb.cget("text"))
    subtype = dropdown_clicked.get()
    converter.convert_wav_to_subtype(carrier_path, subtype)
    

# open button
open_button = ttk.Button(encode_box, text='Select carrier file', command = select_carrier)
open_button2 = ttk.Button(encode_box, text = 'Select plaintext', command = select_plaintext)
encode_button = ttk.Button(tab1, text = 'Start LSB encoding', command = start_lsb_encoding_in_bg)
encode_button2 = ttk.Button(tab1, text = 'Start FFT encoding', command = start_fft_encoding_in_bg)
decode_button = ttk.Button(tab1, text = 'Start LSB decoding', command = start_lsb_decoding_in_bg)
decode_button2 = ttk.Button(tab1, text = 'Start FFT decoding', command = start_fft_decoding_in_bg)
encoded_button = ttk.Button(decode_box, text = 'Select encoded file', command = select_encoded_file)
convert_button = ttk.Button(tab2, text = 'Convert to subtype', command = subtype_convert)


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

pb = ttk.Progressbar(root, orient='horizontal', mode='indeterminate', length=280)

encoding_label.pack(pady=5)
decoding_label.pack(pady=5)
carrier_tb.pack(pady=3)
open_button.pack()
plaintext_tb.pack()
open_button2.pack()
embedded_tb.pack(pady=2)
encoded_button.pack()
key_label.pack(pady=5)
key_tb.pack(pady=3)
offset_label.pack(pady=5)
offset_tb.pack(pady=2)
iv_del_label.pack(pady=2)
iv_delimiter_tb.pack(pady=2)
ct_del_label.pack(pady=2)
ct_delimiter_tb.pack(pady=2)

offset_tb.pack(pady=2)
encode_button.pack(pady=2)
encode_button2.pack(pady=2)
decode_button.pack(pady=2)
decode_button2.pack(pady=2)
drop.pack(pady=2)
convert_button.pack(pady=2)



# run the application
root.mainloop()