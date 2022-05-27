import scipy.io.wavfile as wavfile
import scipy.fftpack as fftpk
from matplotlib import pyplot as plt
from amplitude_operations import amplitude_decoding
from licenta import get_folder_from_path
decoded_bits_fft = []
decoded_string_fft = ""
decoded_string_ifft = ""
decoded_string_stego = ""
decoded_bits = []
decoded_string = ""
decoded_bit = 0

#maybe add message length to UI?
def decode_string(fft, message_length):
    decoded_bit = 0
    decoded_string = ""

    for i, amplitude in enumerate(fft):
        if i >= message_length * 8:
            break
        decoded_bit = amplitude_decoding(amplitude[0].real)
        #print("Decoded bit ", decoded_bit, "from ", freqs[i], "with amplitude", amplitude[0].real)
        decoded_bits_fft.append(decoded_bit)

    for j in range(0,len(decoded_bits_fft),8):
        decoded_byte = "".join(map(str,decoded_bits_fft[j:j+8]))
        if decoded_byte == "¬":
            break
        decoded_string += chr(int(decoded_byte, 2))
    return decoded_string


def fft_decoder(carrier_path):

    s_rate2, signal2 = wavfile.read(carrier_path)
    ch_count2 = signal2.shape[1]
    #print(f"Stego file number of channels = {ch_count2}")
    length2 = signal2.shape[0] / s_rate2
    #print(f"Stego file length = {length2}s")

    fft2 = fftpk.fft(signal2)
    decoded_string_stego = decode_string(fft2, 50)
    recoveredtext_path = get_folder_from_path(carrier_path) + "/recovered.txt"
    print("Decoded string after fft on stego file:", decoded_string_stego[0:50])


    #freqs2 = fftpk.fftfreq(len(fft2), (1.0/s_rate2))
    # plt.plot(freqs2[range(len(fft2)//2)], fft2[range(len(fft2)//2)])                                                          
    # plt.xlabel('Frequency (Hz)')
    # plt.ylabel('Amplitude')
    # plt.show()