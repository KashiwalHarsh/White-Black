from flask import Flask, render_template, request

app=Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/encode',methods=['GET'])
def application():
    return render_template("encode.html")

@app.route('/decode',methods=['GET'])
def about():
    return render_template("decode.html")

@app.route('/about',methods=['GET'])
def about():
    return render_template("about.html")

# @app.route('/analyze', methods=['GET','POST'])
# def new():
#     if request.method=='POST':
#         rawtext=request.form['rawtext']
#         summary,originaltext,len_o,len_s,score=summarizer(rawtext)

#         return render_template('summary.html',summary=summary,originaltext=originaltext,len_o=len_o,len_s=len_s,score=score)

if __name__ == '__main__':
    app.run(debug=False,port=8001)