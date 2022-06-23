from soundfile import read, write

def convert_wav_to_subtype(path, subtype_string):
    data, s_rate = read(path)
    write(path, data, s_rate, subtype = subtype_string)
