from flask import render_template, request, Blueprint
from customerupload.process_input import ProcessInput

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')

@main.route("/process")
def process():
    processor = ProcessInput(ProcessInput.UNPROCESSED_PATH + "input-sample.tsv")
    processed_rows = processor.execute()
    return render_template('complete.html', processed_rows=processed_rows)
