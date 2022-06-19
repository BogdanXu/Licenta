import scipy.io.wavfile as wavfile
import scipy.fftpack as fftpk
from matplotlib import pyplot as plt
from amplitude_operations import amplitude_decoding
from licenta import get_folder_from_path


def decode_string(fft):
    decoded_bit = 0
    decoded_string = ""
    decoded_bits_fft = []

    for i, amplitude in enumerate(fft):
        # if i >= message_length * 8:
        #     break
        decoded_bit = amplitude_decoding(amplitude[0].real)
        decoded_bits_fft.append(decoded_bit)

    for j in range(0,len(decoded_bits_fft),8):
        decoded_byte = "".join(map(str,decoded_bits_fft[j:j+8]))
        decoded_char = chr(int(decoded_byte, 2))
        if decoded_char == '¬':
            return decoded_string
        else:
            decoded_string += decoded_char



def fft_decoder(carrier_path):
    decoded_string_stego = ""
    s_rate2, signal2 = wavfile.read(carrier_path)

    fft2 = fftpk.rfft(signal2)
    decoded_string_stego = decode_string(fft2)
    recoveredtext_path = get_folder_from_path(carrier_path) + "/recovered.txt"

    with open(recoveredtext_path, 'w') as f:
        f.write(decoded_string_stego)
        f.close()
