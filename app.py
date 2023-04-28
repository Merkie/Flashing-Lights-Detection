import os
import uuid
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from process_video import process_video

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video uploaded.'}), 400
    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({'error': 'No file selected.'}), 400
    file_ext = os.path.splitext(video_file.filename)[1]
    random_file_name = f"{uuid.uuid4()}{file_ext}"
    filename = secure_filename(random_file_name)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    chunk_size = 4096
    with open(file_path, 'wb') as f:
        while True:
            chunk = video_file.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)

    # Process the uploaded video file
    video_processing_result = process_video(file_path, threshold=int(request.form.get('threshold')), downscale=float(request.form.get('downscale')))

    # Delete the video file after processing
    os.remove(file_path)

    if 'error' in video_processing_result:
        return jsonify(video_processing_result), 400
    else:
        return jsonify(video_processing_result), 200

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploads/'
    app.run()
