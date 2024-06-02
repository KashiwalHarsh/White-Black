from flask import Flask, render_template, request, jsonify,send_file
import os
from encode import main_encode
from decode import main_decode

app=Flask(__name__)

# Ensure the content directory exists
CONTENT_FOLDER = 'content'
if not os.path.exists(CONTENT_FOLDER):
    os.makedirs(CONTENT_FOLDER)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/encode',methods=['GET'])
def encode():
    return render_template("encode.html")

@app.route('/decode',methods=['GET'])
def decode():
    return render_template("decode.html")

@app.route('/about',methods=['GET'])
def about():
    return render_template("about.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:

        # Save the file to the content directory
        filename = file.filename
        filepath = os.path.join(CONTENT_FOLDER, filename)
        file.save(filepath)

        content = file.read().decode('utf-8')
        # print(content)

        return jsonify({"message": "File successfully uploaded", "content": content}), 200
    return jsonify({"error": "File upload failed"}), 500

@app.route('/input-key', methods=['POST'])
def input_key():
    data = request.json
    key = data.get('key')

    if not key:
        return jsonify({"error": "Key is missing"}), 400
    
    # Here you can call your Python script with the key
    # For demonstration, we're just returning the key
    # Replace this with your actual script call
    newkey = key.encode('utf-8')[:16].ljust(16, b'\0')

    input_key = os.path.join(CONTENT_FOLDER, 'input_key.txt')
    with open(input_key, 'w') as key_file:
        key_file.write(newkey.decode('utf-8'))

    return jsonify({"message": "Input Key received", "key": key})


@app.route('/output-key', methods=['POST'])
def output_key():
    data = request.json
    key = data.get('key')

    if not key:
        return jsonify({"error": "Key is missing"}), 400
    
    newkey = key.encode('utf-8')[:16].ljust(16, b'\0')

    input_key = os.path.join(CONTENT_FOLDER, 'output_key.txt')
    with open(input_key, 'w') as key_file:
        key_file.write(newkey.decode('utf-8'))

    return jsonify({"message": "Output Key received", "key": key})


@app.route('/performEncryption', methods=['GET','POST'])
def perform_encryption():

    main_encode()
    image_path = os.path.join(CONTENT_FOLDER, 'binary_image.png')

    return send_file(image_path, as_attachment=True)

@app.route('/performDecryption', methods=['GET','POST'])
def perform_decryption():

    main_decode()
    text_path = os.path.join(CONTENT_FOLDER, 'output.txt')

    return send_file(text_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=False)