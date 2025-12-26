from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from pathlib import Path
from rag_chatbot_pipe import main
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / 'files'
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.route('/')
def start():
    UPLOAD_DIR = Path("files")

    files = [f for f in UPLOAD_DIR.iterdir() if f.is_file()]

    if len(files) == 1:
        files[0].unlink()
    
    return jsonify({"message": 'API ready', "status": "ok"})

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'message': 'Missing file field.'})

    f = request.files['file']
    
    filename = secure_filename(f.filename)
    save_path = UPLOAD_DIR / filename
    
    f.save(save_path)

    return jsonify({
        "status": "uploaded",
        "filename": save_path.name,
        "path": str(save_path),
        "size_bytes": save_path.stat().st_size
    })
    
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    q = data.get('question')
    
    response = main(q)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
