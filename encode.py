from Crypto.Cipher import AES
from PIL import Image
from Crypto.Random import get_random_bytes
import os


#Encrypt text to AES cypher
def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        data = file.read()

    # Generate a random initialization vector
    iv = get_random_bytes(AES.block_size)

    # Create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Encrypt the data
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))

    # Write the encrypted data along with the initialization vector to a new file
    with open('encrypted.txt', 'wb') as encrypted_file:
        encrypted_file.write(iv + encrypted_data)

    print("Encryption successful : 'encrypted.txt'.")

def pad(s, bs):
    return s + (bs - len(s) % bs) * chr(bs - len(s) % bs).encode()

#Encrypted text to binary
def encrypted_to_binary(file_path_encrypted):
    # Read the content of the encrypted file
    with open(file_path_encrypted, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    # Convert the encrypted data into binary representation
    binary_data = ''.join(format(byte, '08b') for byte in encrypted_data)

    # Write the binary representation to a new file
    with open('binary-rep.txt', 'w') as binary_file:
        binary_file.write(binary_data)

    print("Binary Conversion succesful : 'binary-rep.txt'.")

# Conversion of Binary to Image
def binary_to_image(binary_data, output_file):
    # Calculate width and height based on the length of the binary data
    length = len(binary_data)
    width = int(length ** 0.5)  # Square root of the length for a square image
    height = (length + width - 1) // width  # Ensure all data is used, even if not a perfect square
    
    # Create a new image with the calculated dimensions
    img = Image.new('1', (width, height))
    
    # Convert binary data to a list of integers
    pixel_data = [int(bit) * 255 for bit in binary_data]
    
    # Set the pixel values in the image
    img.putdata(pixel_data)
    
    print("Image Formation succesful : 'binary_image.png'.")
    # Save the image to a file
    img.save(output_file)


#---------------------------------------------------------------------------


# Encryption
file_path = 'file.txt'
key = b'ThisIsASecretKey'
encrypt_file(file_path, key)

# Binary Rep of Encrypted text
file_path_encrypted = 'encrypted.txt'
encrypted_to_binary(file_path_encrypted)

# Conversion of Binary into Image
# Read binary data from file
with open("binary-rep.txt", "r") as file:
    binary_data = file.read().strip()

output_file = "binary_image.png"

binary_to_image(binary_data, output_file)