import librosa
import soundfile

data, s_rate = soundfile.read('Resources/ur_mocking_me.wav')
print(s_rate)
soundfile.write('Resources/ur_mocking_me.wav', data, s_rate, subtype = 'FLOAT')