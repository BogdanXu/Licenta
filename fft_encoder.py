import scipy.io.wavfile as wavfile
import numpy as np
from scipy.fft import fft, ifft, irfft
import amplitude_operations
from licenta import get_folder_from_path, transform_string_to_bits
import scipy.fftpack as fftpk
from matplotlib import pyplot as plt

def fft_encoder(carrier_path, stego_message):

    #Reading the complex values of the signal
    s_rate, signal = wavfile.read(carrier_path)
    ch_count = signal.shape[1]
    length = signal.shape[0] / s_rate
    y = []
    y_inv = []
    recovered_y = []
    bits = transform_string_to_bits(stego_message)
    decoded_bits = []
    decoded_string = ""
    #Starting encoding
    #Splitting the signal into bytes in order to apply FFT on each byte # splitting is useless, just fft the whole thing
    # for i in range(0, len(signal), 8):
    #     y.extend(fft(signal[i:i+8])) 
    y = fftpk.rfft(signal)

    #Appending the bits of the message to the FFT signal
    for i in range(0, len(bits)):
        y[i][0] = amplitude_operations.amplitude_encoding(y[i][0], bits[i])
    #print("Embedded " + str(bits) " bits into a carrier that has a size of " + str(len(signal)))

    #Checking the encoded message
    # for i in range(0, len(signal)):
    #     decoded_bit = teste.amplitude_decoding(y[i][0])
    #     decoded_bits.append(decoded_bit)
    # for j in range(0,len(decoded_bits),8):
    #     decoded_char = "".join(map(str,decoded_bits[j:j+8]))
    #     decoded_string += chr(int(decoded_char, 2))
    # print(decoded_string[0:50])

    #Doing the Inverse FFT
    y_inv.extend(irfft(y))

    #Write the embedded data to the output .wav file
    embedded_audio_path = get_folder_from_path(carrier_path) + "/embedded_audio.wav"
    data = np.array(y_inv, dtype=signal.dtype)
    wavfile.write(embedded_audio_path, s_rate, data)




# Graph of FFT of modified audio file
# fft2 = fftpk.fft(signal)
# freqs = fftpk.fftfreq(len(fft2), (1.0/s_rate))

# plt.plot(freqs[range(len(fft2)//2)], fft2[range(len(fft2)//2)])
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Amplitude')
# plt.show()