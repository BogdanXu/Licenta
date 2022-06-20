import soundfile

data, s_rate = soundfile.read('Resources/ur_mocking_me.wav')
print(soundfile.available_subtypes('WAV'))
soundfile.write('Resources/ur_mocking_me.wav', data, s_rate, subtype = 'FLOAT')

def convert_wav_to_subtype(path, subtype_string):
    data, s_rate = soundfile.read(path)
    soundfile.write(path, data, s_rate, subtype = subtype_string)
