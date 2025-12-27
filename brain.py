from werkzeug.utils import secure_filename
from pathlib import Path
from rag_chatbot_pipe import main
import json

def upload(file):
    return 'Status: ok'

def ask(q, file_path):
    response = main(q, file_path)
    
    return response
