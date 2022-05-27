import scipy.io.wavfile as wavfile
from scipy.fft import fft, ifft
from matplotlib import pyplot as plt
from licenta import transform_string_to_bits
import numpy as np
import amplitude_operations
import scipy.fftpack as fftpk

s_rate, signal = wavfile.read("Resources/fft_stego.wav")
ch_count = signal.shape[1]
length = signal.shape[0] / s_rate
recovered_y = []
decoded_bits = []
decoded_string = ""

#Starting decoding
#FFT on stegofile
for i in range(0, len(signal), 8):
    recovered_y.extend(fft(signal[i:i+8]))

#Recover the secret message
for i in range(0, len(signal)):
    decoded_bit = amplitude_operations.amplitude_decoding(recovered_y[i][0])
    decoded_bits.append(decoded_bit)

for j in range(0,len(decoded_bits),8):
    decoded_char = "".join(map(str,decoded_bits[j:j+8]))
    decoded_string += chr(int(decoded_char, 2))
print(decoded_string[0:50])

#print("Decoded string:", decoded_string)

fft2 = fftpk.fft(signal)
freqs = fftpk.fftfreq(len(fft2), (1.0/s_rate))

plt.plot(freqs[range(len(fft2)//2)], fft2[range(len(fft2)//2)])                                                          
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()









