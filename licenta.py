import wave
import zlib
from crypto_functions import OFB_decrypt, OFB_encrypt
# string -> unicode -> binary -> strip -> justify -> join each bit with a string and apply int to int -> list of every bit
def transform_string_to_bits(string):
    bits = []
    for i in string:
        binary_value = bin(ord(i))
        binary_value = ''.join(binary_value.lstrip('0b').rjust(8,'0'))
        for bit in binary_value:
            bits.append(int(bit))
    return bits


def get_frames(extracted):
    delimiter_char = '#'
    delimiter_array = transform_string_to_bits(delimiter_char)
    delimiter_array = "".join(map(str, delimiter_array[0:len(delimiter_array)]))
    decoded_string = ""
    decoded_byte = b''

    for i in range(0,len(extracted),8):
        decoded_byte = "".join(map(str,extracted[i:i+8]))
        if decoded_byte == delimiter_array:
            return decoded_string
        decoded_string += chr(int(decoded_byte, 2))


    
def LSB_encode(string):

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

def LSB_decode():
    audio_file = wave.open("audio_file_embedded.wav", mode='rb')
    frame_bytes = bytearray(list(audio_file.readframes(audio_file.getnframes())))

    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    decoded = get_frames(extracted)
    #print("Sucessfully decoded: "+decoded)
    audio_file.close()
    return decoded


if __name__ == "__main__":

    reader = open("book.txt", "r", encoding="utf-8")
    plaintext = reader.read()
    writer = open("decrypted.txt", "w", encoding="utf-8")
    #plaintext = "Super secret message, very long, very big, very secret, very message"
    key = "abcdefghabcdefgh"
    compressed_text = zlib.compress(bytes(plaintext, 'utf-8'))
    ciphertext = OFB_encrypt(compressed_text, key)
    LSB_encode(ciphertext[1])

    decoded = LSB_decode()
    text = OFB_decrypt((ciphertext[0], decoded), "abcdefghabcdefgh")

    
    print("Length of plaintext:", len(plaintext))
    print("Length of plaintext after compression: ", str(len(text)))

    decompressed_value = zlib.decompress(text)

    writer.write(str(decompressed_value, 'utf-8'))

    reader.close()
    writer.close()
    #print(str(decompressed_value, 'utf-8'))