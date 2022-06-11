import scipy.io.wavfile as wavfile
from matplotlib import pyplot as plt
from licenta import transform_string_to_bits
import numpy as np
import amplitude_operations
import scipy.fftpack as fftpk

def generate_sine_wave(freq, sample_rate, duration):
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * freq
    # 2pi because np.sin takes radians
    y = np.sin((2 * np.pi) * frequencies)
    return x, y

SAMPLE_RATE = 44100  # Hertz
DURATION = 5  # Seconds

s_rate, signal = wavfile.read("Resources/fft_stego.wav")
ch_count = signal.shape[1]
length = signal.shape[0] / s_rate
recovered_y = []
decoded_bits = []
decoded_string = ""

x, y = generate_sine_wave(2, SAMPLE_RATE, DURATION)
plt.plot(x, y)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.show()


_, nice_tone = generate_sine_wave(200, SAMPLE_RATE, DURATION)
_, noise_tone = generate_sine_wave(2000, SAMPLE_RATE, DURATION)
noise_tone = noise_tone * 0.2

mixed_tone = nice_tone + noise_tone

normalized_tone = np.int16((mixed_tone / mixed_tone.max()) * 32767)
plt.plot(normalized_tone[:1000])
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.show()

#FFT on stegofile #useless, just do line 48
# for i in range(0, len(signal), 8):
#     recovered_y.extend(fftpk.rfft(signal[i:i+8]))


fft2 = fftpk.rfft(signal)
freqs = fftpk.rfftfreq(len(fft2), (1.0/s_rate))

plt.plot(freqs[range(len(fft2)//2)], fft2[range(len(fft2)//2)])                                                          
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()

N = SAMPLE_RATE * DURATION

yf = fftpk.rfft(normalized_tone)
xf = fftpk.rfftfreq(N, 1 / SAMPLE_RATE)

plt.plot(xf, np.abs(yf))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.show()