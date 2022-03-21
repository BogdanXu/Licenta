import scipy.io.wavfile as wavfile
import scipy.fftpack as fftpk
from matplotlib import pyplot as plt
from licenta import transform_string_to_bits
import numpy as np
from teste import amplitude_decode, amplitude_encoding

def decode_string(fft):
    decoded_bit = 0
    decoded_string = ""
    decoded_bits = []
    for i, amplitude in enumerate(fft):
        decoded_bit = amplitude_decode(amplitude[0].real)
        #print("Decoded bit ", decoded_bit, "from ", freqs[i], "with amplitude", amplitude[0].real)
        decoded_bits.append(decoded_bit)

    for j in range(0,len(decoded_bits),8):
        decoded_char = "".join(map(str,decoded_bits[j:j+8]))
        if "#" in chr(int(decoded_char, 2)):
            break
        decoded_string += chr(int(decoded_char, 2))
    return decoded_string

s_rate, signal = wavfile.read("piano.wav")
ch_count = signal.shape[1]
#print(f"number of channels = {ch_count}")
length = signal.shape[0] / s_rate
#print(f"length = {length}s")

fft = fftpk.fft(signal)
freqs = fftpk.fftfreq(len(fft), (1.0/s_rate))
secret_message = "Super secret message.#"
bits = transform_string_to_bits(secret_message)

for i, amplitude in enumerate(fft):
    #print("Modified the amplitude of frequency ", freqs[i], "from ", amplitude[0].real, "to")
    if i<len(bits):
        amplitude[0] = amplitude_encoding(amplitude[0].real, bits[i])
    #print(amplitude)


decoded_string_fft = decode_string(fft)
print("Decoded string before ifft: ",decoded_string_fft[0:50])


ifft = fftpk.ifft(fft)

wavfile.write("fft_stego.wav", s_rate, ifft.astype(signal.dtype))

plt.plot(freqs[range(len(fft)//2)], fft[range(len(fft)//2)])                                                          
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()









