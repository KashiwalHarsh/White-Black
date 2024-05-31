from flask import Flask, render_template, request, jsonify
import os

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

# @app.route('/analyze', methods=['GET','POST'])
# def new():
#     if request.method=='POST':
#         rawtext=request.form['rawtext']
#         summary,originaltext,len_o,len_s,score=summarizer(rawtext)

#         return render_template('summary.html',summary=summary,originaltext=originaltext,len_o=len_o,len_s=len_s,score=score)

if __name__ == '__main__':
    app.run(debug=True,port=8001)