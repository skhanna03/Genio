from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

GENIO_FOLDER = '/Users/aumkarrenavikar/Downloads/Genio/'

@app.route('/members')
def members():
    return {"members": ["Member1", "Member2", "Member3"]}

@app.route('/upload', methods=['POST'])
def upload_file():
    text = request.form['text']

    # Process the text as needed
    # ...

    # Here, we assume the audio file is pre-generated and stored in the Genio folder
    # For this example, the filename is 'Test.wav'
    audio_file_path = 'Test.wav'

    # Return the URL for the audio file
    return jsonify(audioFile=f'/audio_files/{audio_file_path}')

@app.route('/audio_files/<filename>')
def audio_files(filename):
    return send_from_directory(GENIO_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
