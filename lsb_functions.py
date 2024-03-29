import wave
import numpy as np

iv_delimiter = "695" #add this later to GUI
ct_delimiter = "125" #this too
offset = 2


def get_folder_from_path(path):
    slash_index = path.rfind('/')
    return path[0:slash_index]


# string -> unicode -> binary -> strip -> justify -> join each bit with a string and cast to int -> put each bit in a list
def transform_string_to_bits(string):
    bits = []
    for i in string:
        binary_value = bin(ord(i))
        binary_value = ''.join(binary_value.lstrip('0b').rjust(8,'0'))
        for bit in binary_value:
            bits.append(int(bit))
    return bits

#not used for now
def encode_positions(max_length, number_of_positions, key):
    positions = []
    seed = 0
    for c in key:
        seed += ord(c)
    rng = np.random.default_rng(seed)
    positions = rng.integers(low=0, high=number_of_positions, size=max_length)
    return positions
    

#Gets an array of last significant bits and decodes IV and ciphertext from it
def get_frames(extracted, iv_delimiter, ct_delimiter):

    result = ["", ""]
    decoded_string = ""
    decoded_byte = b''
    found_iv, found_ct = False, False


    for i in range(0,len(extracted),8):
        decoded_byte = "".join(map(str,extracted[i:i+8]))
        decoded_string += chr(int(decoded_byte, 2))

    if iv_delimiter in decoded_string:
        iv_index = decoded_string.index(iv_delimiter)
        iv = decoded_string[0:iv_index]
        index_ct_start = iv_index + len(iv_delimiter)
        result[0] = iv
        found_iv = True
    
    if ct_delimiter in decoded_string:
        index_ct_end = decoded_string.rindex(ct_delimiter)
        ct = decoded_string[index_ct_start:index_ct_end]
        result[1] += ct
        found_ct = True

    if found_iv and found_ct:
        print(tuple(result))
        return tuple(result)


#Encodes the IV and the ciphertext in the audio file  
def LSB_encode(iv, string, original_audio_path, embedded_audio_path, offset, iv_delimiter, ct_delimiter):

    audio_file = wave.open(original_audio_path, mode='rb')
    frame_bytes = bytearray(list(audio_file.readframes(audio_file.getnframes())))
    
    print("Number of frame_bytes is", len(frame_bytes))
    
    string = iv + iv_delimiter + string + ct_delimiter

    bits = transform_string_to_bits(string)                                                       
    # Replace LSB of each byte of the audio data by one bit from the text bit array
    for i, bit in enumerate(bits):
        frame_bytes[i*offset] = (frame_bytes[i*offset] & 254) | bit
    # Get the modified bytes
    frame_modified = bytes(frame_bytes)

    # Write bytes to a new wave audio file
    with wave.open(embedded_audio_path, 'wb') as fd:
        fd.setparams(audio_file.getparams())
        fd.writeframes(frame_modified)
    audio_file.close()
    print("Finished encoding")

#Decodes the IV and the ciphertext in the audio file
def LSB_decode(embedded_audio_path, offset, iv_delimiter, ct_delimiter):
    audio_file = wave.open(embedded_audio_path, mode='rb')
    frame_bytes = bytearray(list(audio_file.readframes(audio_file.getnframes())))

    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes)) if i%offset==0]
    decoded = get_frames(extracted, iv_delimiter, ct_delimiter)
    print("Sucessfully decoded: ", decoded)
    audio_file.close()
    print("Finished decoding")
    return decoded
