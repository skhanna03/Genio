from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/members')
def members():
    return {"members": ["Member1", "Member2", "Member3"]}

@app.route('/upload', methods=['POST'])
def upload_file():
    text = request.form['text']
    video = request.files['video']

    # Here, you would process the text and video
    # For example, save the video and perform any required operations

    # Just as an example, let's assume we save the video and create a dummy audio file
    video_filename = os.path.join('/Users/aumkarrenavikar/Downloads/Genio/', video.filename)
    video.save(video_filename)

    # Create or fetch an audio file based on the text
    # For now, this will just be a placeholder string
    audio_file_path = '/Users/aumkarrenavikar/Downloads/Genio/Test.wav'

    # Return the path or URL of the audio file
    return {'audioFile': audio_file_path}

if __name__ == '__main__':
    app.run(debug=True)
