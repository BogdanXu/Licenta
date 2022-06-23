import struct

def float_to_bin(num):
    return format(struct.unpack('!I', struct.pack('!f', num))[0], '064b')

def bin_to_float(binary):
    return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]

#The 10th bit from the end of the binary representation seems to work the best for now, encoding there
def amplitude_encoding(amplitude, bit):
    encoded_amplitude = float_to_bin(amplitude)
    encoded_amplitude = encoded_amplitude[:-10] + str(bit) + encoded_amplitude[-9:]
    encoded_amplitude = bin_to_float(encoded_amplitude)
    return encoded_amplitude

def amplitude_decoding(amplitude):
    decoded_amplitude = float_to_bin(amplitude)
    decoded_bit = decoded_amplitude[-10]
    return int(decoded_bit)

amplitude = 0.0
encoded_amplitude = amplitude_encoding(amplitude, 1)
print(encoded_amplitude)
bit = amplitude_decoding(encoded_amplitude)
print(bit)
