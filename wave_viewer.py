import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wavfile
import scipy.fftpack as fftpk

s_rate, signal = wavfile.read("Resources/embedded_audio.wav")
ch_count = signal.shape[1]
length = len(signal)/s_rate
#Get time from indices
print("wav file has " + str(len(signal)) + " elements in each of its " + str(ch_count) + " channels")

fft2 = fftpk.rfft(signal)
freqs = fftpk.rfftfreq(len(fft2), (1.0/s_rate))
print("fft of wav file has " + str(len(fft2)) + " elements in each of its " + str(ch_count) + " channels")

time = np.arange(0, length, 1/s_rate)
#Plot
plt.title('audio file, 2 channels, 4,108,858 bytes')
plt.plot(time, signal)
# plt.plot(signal[0:10240][1])
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

# for channel in channels:
#     plt.plot(Time,channel)
plt.show()

plt.title('FFT of embedded audio file, 2 channels, 4,108,858 bytes')
plt.plot(freqs, fft2)
# plt.plot(signal[0:10240][1])
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude')

# for channel in channels:
#     plt.plot(Time,channel)
plt.show()