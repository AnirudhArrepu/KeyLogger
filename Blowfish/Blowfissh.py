from SandPboxes import s
from SandPboxes import p
encrypt_p = p.copy()
decrypt_p = p.copy()

def hex_xor(hex_str1, hex_str2):
    # Convert the input hexadecimal strings to integers and perform the XOR operation
    int_value_hex1 = int(hex_str1, 16)
    int_value_hex2 = int(hex_str2, 16)
    result_hex_xor = int_value_hex1 ^ int_value_hex2
    # Format the result as a 2-character hexadecimal string
    return format(result_hex_xor, '02x')

def FiestelFunction(a):
    a = int(a, 16)
    result1 = (s[0][a >> 24] + s[1][(a >> 16) & 0xFF]) & 0xFF
    result1 ^= s[2][(a >> 8) & 0xFF]
    result1 = (result1 + s[3][a & 0xFF]) & 0xFF
    # Format the result as a 2-character hexadecimal string
    return format(result1, '02x')

def InverseFiestelFunction(a_hex):
    result1 = int(a_hex, 16)
    result1 = (result1 - s[3][result1 & 0xFF]) & 0xFF
    result1 ^= s[2][(result1 >> 8) & 0xFF]
    result1 = (result1 - s[0][(result1 >> 24)]) & 0xFF
    result1 = (result1 - s[1][(result1 >> 16) & 0xFF]) & 0xFF
    # Format the result as a 2-character hexadecimal string
    return format(result1, '02x')

def generating_subkeys(key, t):
    subkeys = []
    while key > 0:
        subkey = key & 0xFFFFFFFF
        subkeys.append(format(subkey, '08x'))
        key >>= 32
    subkeys.reverse()
    t[:len(subkeys)] = subkeys

def encrypt(string, key, p):
    # Initialize the subkeys
    generating_subkeys(key, p)

    # Split the 64-bit input into left and right halves
    left = string >> 32
    right = string & 0xFFFFFFFF

    for i in range(16):
        left, right = right, hex_xor(left, FiestelFunction(right) ^ p[i])

    # Swap left and right one more time before the final XORs
    left, right = right, left

    # Perform the final XORs with the last two subkeys
    right = hex_xor(right, p[16])
    left = hex_xor(left, p[17])

    # Convert the left and right halves back to integers and combine them
    left = int(left, 16)
    right = int(right, 16)
    encrypted_result = (left << 32) | right

    return encrypted_result

def decrypt(string, key, p):
    # Initialize the subkeys
    generating_subkeys(key, p)

    # Split the 64-bit input into left and right halves
    left = string >> 32
    right = string & 0xFFFFFFFF

    # Perform the final XORs in reverse order
    right = hex_xor(right, p[16])
    left = hex_xor(left, p[17])

    # Swap left and right one more time before the inverse Fiestel function
    left, right = right, left

    for i in range(15, -1, -1):
        left, right = right, hex_xor(left, InverseFiestelFunction(right) ^ p[i])

    # Convert the left and right halves back to integers and combine them
    left = int(left, 16)
    right = int(right, 16)
    decrypted_result = (left << 32) | right

    return decrypted_result

# Input and testing
encrypt_key = int(input("Enter the encryption key in hexadecimal format (e.g., 0x123456789ABCDEF0): "), 16)
encrypt_input = int(input("Enter the input to encrypt in hexadecimal format: "), 16)

encrypted_result = encrypt(encrypt_input, encrypt_key, encrypt_p)

print("Encrypted Result (in hex): 0x{:016X}".format(encrypted_result))

decrypt_key = int(input("Enter the decryption key in hexadecimal format: "), 16)
decrypt_input = int(input("Enter the encrypted input to decrypt in hexadecimal format: "), 16)

decrypted_result = decrypt(decrypt_input, decrypt_key, decrypt_p)

print("Decrypted Result (in hex): 0x{:016X}".format(decrypted_result))
