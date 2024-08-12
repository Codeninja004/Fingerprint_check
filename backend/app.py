import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from third import checkFingerPrint

database_path = r"backend\original"
testImg = r"backend\test\Image002.bmp"

UPLOAD_FOLDER = 'test'
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'bmp'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.secret_key = 'secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)



@app.route("/",methods=['GET'])
def test():
    if request.method == "GET":
        return "Working OK!" ,201
    


@app.route("/test",methods=['GET'])
def books():
    if request.method == 'GET':
        result = checkFingerPrint(testImg,database_path)
        return jsonify(result), 200
    else: 
        return jsonify({" Could not"}), 500


@app.route("/media/upload", methods=["POST"])
def upload_media():
    if request.method == 'POST':
        response = jsonify(message="Simple server is running")
        response.headers.add("Access-Control-Allow-Origin", "*")
        target=os.path.join(UPLOAD_FOLDER)
        if not os.path.isdir(target):
            os.mkdir(target)
        file = request.files['file'] 
        filename = secure_filename(file.filename)
        destination="/".join([target, filename])
        file.save(destination)
        result = checkFingerPrint(destination,database_path)
        os.remove(destination)
        if(result == "Not found"):
            return jsonify({"message":"Finger Print not found"}),202
        return jsonify({"message":"FingerPrint Matched score: ",'score':result}), 200


@app.route("/media/upload/new", methods=["POST"])
def upload_new_media():
    if request.method == 'POST':
        response = jsonify(message="Simple server is running")
        response.headers.add("Access-Control-Allow-Origin", "*")
        target=os.path.join(database_path)
        if not os.path.isdir(target):
            os.mkdir(target)
        file = request.files['file'] 
        filename = secure_filename(file.filename)
        destination="/".join([target, filename])
        file.save(destination)
        return jsonify({"message":"FingerPrint Uploaded Successfull"}), 200
    
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)