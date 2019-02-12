import os
import time
from flask import render_template, request, redirect, Blueprint
from customerupload.process_input import ProcessInput
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)

@main.route("/")
def home():
    return render_template('home.html')

@main.route('/upload', methods=['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
        file = request.files['file']
        start_time = time
        file_path = os.path.join(ProcessInput.UNPROCESSED_PATH,
                                 start_time.strftime("%Y%m%d-%H%M%S") + '.tsv')
        if not os.path.exists(ProcessInput.UNPROCESSED_PATH):
            os.makedirs(ProcessInput.UNPROCESSED_PATH)
        file.save(file_path)
        
        processor = ProcessInput(file_path, start_time)
        processed_rows = processor.execute()
        return render_template('complete.html', processed_rows=processed_rows)
