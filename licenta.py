import wave

# string -> unicode -> binary -> strip -> justify -> join each bit with a string and apply int to int -> list of every bit
def transform_string_to_bits(string):
    bits = []
    for i in string:
        binary_value = bin(ord(i))
        binary_value = ''.join(binary_value.lstrip('0b').rjust(8,'0'))
        for bit in binary_value:
            bits.append(int(bit))
    return bits


def get_decrypted_frames(extracted):
    delimiter_char = '#'
    #string = "".join(chr(int("".join(map(str,extracted[i:i+8])) ,2)) for i in range(0,len(extracted),8))

    delimiter_array = transform_string_to_bits(delimiter_char)
    delimiter_array = "".join(map(str, delimiter_array[0:len(delimiter_array)]))
    decoded_string = ""
    decoded_byte = b''

    for i in range(0,len(extracted),8):
        decoded_byte = "".join(map(str,extracted[i:i+8]))
        if decoded_byte == delimiter_array:
            return decoded_string
        decoded_string += chr(int(decoded_byte, 2))


    
def LSB_encrypt(string):

    audio_file = wave.open("audio_file.wav", mode='rb')
    frame_bytes = bytearray(list(audio_file.readframes(audio_file.getnframes())))

    string = string + 2 * '#'

    bits = transform_string_to_bits(string)                                                       
    # Replace LSB of each byte of the audio data by one bit from the text bit array
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    # Get the modified bytes
    frame_modified = bytes(frame_bytes)

    # Write bytes to a new wave audio filepy
    with wave.open('audio_file_embedded.wav', 'wb') as fd:
        fd.setparams(audio_file.getparams())
        fd.writeframes(frame_modified)
    audio_file.close()

def LSB_decrypt():
    audio_file = wave.open("audio_file_embedded.wav", mode='rb')
    frame_bytes = bytearray(list(audio_file.readframes(audio_file.getnframes())))

    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    decoded = get_decrypted_frames(extracted)
    print("Sucessfully decoded: "+decoded)
    audio_file.close()


if __name__ == "__main__":
    string='Super secret message that has to be encrypted'
    f = open("1_second_example.txt")
    string = f.read()
    LSB_encrypt(string)
    #LSB_decrypt()