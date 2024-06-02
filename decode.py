from Crypto.Cipher import AES
from PIL import Image
from Crypto.Random import get_random_bytes
import os

OUTPUT_FOLDER = "output-tracer"
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

CONTENT_FOLDER = 'content'
if not os.path.exists(CONTENT_FOLDER):
    os.makedirs(CONTENT_FOLDER)

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

#-----------------------------------------------------------

def main_decode():

    input_key_path = os.path.join(CONTENT_FOLDER, 'output_key.txt')
    # key = b'ThisIsASecretKey'
    with open(input_key_path, 'r') as file:
        key = file.read()

    key = key.encode('utf-8')

    # Conversion of Image into Binary
    input_file = os.path.join(CONTENT_FOLDER, 'binary_image.png')
    output_file = os.path.join(OUTPUT_FOLDER, 'binary-rec.txt')

    image_to_binary(input_file, output_file)

    #Reconstuction of Encrypted file

    binary_file_path = os.path.join(OUTPUT_FOLDER, 'binary-rep.txt')
    output_file_path = os.path.join(OUTPUT_FOLDER, 'reconstructed_encrypted.txt')

    binary_to_encrypted_from_file(binary_file_path, output_file_path)

    #Data Extraction form the Reconstructed Encrpyted file
    encrypted_file_path = os.path.join(OUTPUT_FOLDER, 'reconstructed_encrypted.txt')
    output_file_path = os.path.join(CONTENT_FOLDER, 'output.txt')
    decrypt_file(encrypted_file_path, key, output_file_path)


# Flow
# Text File -> Encrypt with AES -> Convert It into Binary -> Binary to Image

# Image to Binary -> Binary to Encrypted Text -> Decrypt with AES -> Text File

#Message to Self

#use python encode.py to run the encdoing process
#use python decode.py to run the decdoing process

#To Do

#Easy Apprach 1
# Build a UI on top of this exact application
# Encoding Phase
# Takes a Text file as input along with a key to encrypt the data
# Outputs an Image in png format which cointains the data hidden in it
# Decoding Phase 
# Take the image in png format as input along with the same key to decrypt
# Outputs the .txt file which contains the orignal data

#Approach 2
# Create multiple pictures of same long data by modifying the code to output to give multiple pictures
# Create a video out of those images 
# Upload it to Youtbe in full HD

# Download the Video
# Decode it Frame by Frame to get the data encoded in the video