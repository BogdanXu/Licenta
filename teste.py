import struct

def float_to_bin(num):
    return format(struct.unpack('!I', struct.pack('!f', num))[0], '064b')


def bin_to_float(binary):
    return struct.unpack('!f',struct.pack('!I', int(binary, 2)))[0]


def amplitude_encoding(amplitude, bit):
    encoded_amplitude = float_to_bin(amplitude)
    encoded_amplitude = encoded_amplitude[:-5]+str(bit)*5
    encoded_amplitude = bin_to_float(encoded_amplitude)
    return encoded_amplitude



def amplitude_decode(amplitude):
    decoded_amplitude = float_to_bin(amplitude)
    decoded_bit = decoded_amplitude[-3]
    return int(decoded_bit)


amplitude = 0.00011367728
encoded_amplitude = amplitude_encoding(amplitude, 0)
print(encoded_amplitude)
bit = amplitude_decode(encoded_amplitude)
print(bit)


# import base64

# with open("image.png", "rb") as image:
#     b64string = base64.b64encode(image.read())

# print(b64string)


# from PIL import Image
# import io

# decoded = open('decoded.png', 'wb')
# decoded.write(base64.b64decode(b64string))
# decoded.close()
