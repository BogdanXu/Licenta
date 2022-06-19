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
    y = []
    y_inv = []
    stego_message = stego_message + '¬'
    bits = transform_string_to_bits(stego_message)
    
    y = fftpk.rfft(signal)
    y2 = fftpk.rfft(signal)

    #Appending the bits of the message to the FFT signal
    for i in range(0, len(bits)):
        embedded_bit = bits[i]
        y[i][0] = amplitude_operations.amplitude_encoding(y[i][0], embedded_bit)
        y[i][1] = amplitude_operations.amplitude_encoding(y[i][1], embedded_bit)

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