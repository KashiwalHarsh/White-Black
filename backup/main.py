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

# Conversion of Image to Binary
def image_to_binary(input_file, output_file):
    # Open the image file
    img = Image.open(input_file)
    
    # Convert the image to binary data
    binary_data = ''.join([str(int(pixel / 255)) for pixel in img.getdata()])
    
    print("Image Deormation succesful : 'binary-rec.txt'.")
    # Save the binary data to a file
    with open(output_file, "w") as file:
        file.write(binary_data)

# Conversion of Binary into Encrypted Reconstructed
def binary_to_encrypted_from_file(input_file_path, output_file_path):
    # Read binary data from file
    with open(input_file_path, 'r') as binary_file:
        binary_data = binary_file.read()

    # Convert binary data back to bytes
    encrypted_data = bytes(int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8))

    # Write the encrypted data to a file
    with open(output_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)

    print("Encrypted data converted from binary and saved in:", output_file_path)

#Final Output text decrypted
def decrypt_file(encrypted_file_path, key, output_file_path):
    # Read the content of the encrypted file
    with open(encrypted_file_path, 'rb') as encrypted_file:
        encrypted_data = encrypted_file.read()

    # Extract the initialization vector from the encrypted data
    iv = encrypted_data[:AES.block_size]

    # Create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the data
    decrypted_data = cipher.decrypt(encrypted_data[AES.block_size:])

    # Unpad the decrypted data
    decrypted_data = unpad(decrypted_data)

    # Write the decrypted data to a new file
    with open(output_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

    print("Decryption successful. Decrypted data saved in:", output_file_path)

def unpad(s):
    return s[:-ord(s[len(s)-1:])]


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

# Conversion of Image into Binary
input_file = "binary_image.png"
output_file = "binary-rec.txt"

image_to_binary(input_file, output_file)

#Reconstuction of Encrypted file
binary_file_path = 'binary-rep.txt'  # Path to the file containing binary data
output_file_path = 'reconstructed_encrypted.txt'  # Output file path
binary_to_encrypted_from_file(binary_file_path, output_file_path)

#Data Extraction form the Reconstructed Encrpyted file
encrypted_file_path = 'reconstructed_encrypted.txt'
output_file_path = 'data.txt'
decrypt_file(encrypted_file_path, key, output_file_path)