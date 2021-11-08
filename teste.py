string = "c"
print(list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string]))))

extracted = [0, 1, 0, 1, 0, 0, 0, 0]
print(chr(int("".join(map(str,extracted[0:8])),2)))

