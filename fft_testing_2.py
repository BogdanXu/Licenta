import scipy.io.wavfile as wavfile
import numpy as np
from scipy.fft import fft, ifft
import teste
from licenta import transform_string_to_bits
import scipy.fftpack as fftpk
from matplotlib import pyplot as plt

#Reading the complex values of the signal
s_rate, signal = wavfile.read("Resources/piano.wav")
ch_count = signal.shape[1]
length = signal.shape[0] / s_rate
y = []
y_inv = []
recovered_y = []
secret_message = "the umbral choir works in our favour"
bits = transform_string_to_bits(secret_message)
decoded_bits = []
decoded_string = ""

#Starting encoding
#Splitting the signal into bytes in order to apply FFT on each byte
for i in range(0, len(signal), 8):
    y.extend(fft(signal[i:i+8])) 

#Appending the bits of the message to the FFT signal
for i in range(0, len(bits)):
    y[i][0] = teste.amplitude_encoding(y[i][0], bits[i])

#Checking the encoded message
# for i in range(0, len(signal)):
#     decoded_bit = teste.amplitude_decoding(y[i][0])
#     decoded_bits.append(decoded_bit)
# for j in range(0,len(decoded_bits),8):
#     decoded_char = "".join(map(str,decoded_bits[j:j+8]))
#     decoded_string += chr(int(decoded_char, 2))
# print(decoded_string[0:50])

decoded_bits.clear()
del decoded_string
decoded_string = ""


#Doing the Inverse FFT on each byte
for i in range(0, len(y), 8):
    y_inv.extend(ifft(y[i:i+8]))
#Encoding finished

data = np.array(y_inv, dtype=signal.dtype)
wavfile.write("Resources/fft_stego.wav", s_rate, data)


fft2 = fftpk.fft(signal)
freqs = fftpk.fftfreq(len(fft2), (1.0/s_rate))

plt.plot(freqs[range(len(fft2)//2)], fft2[range(len(fft2)//2)])                                                          
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()
