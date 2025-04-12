# 파일 위치: pdfproject/app.py
import os
import shutil
import uuid
from flask import Flask, render_template, request, jsonify, send_from_directory
from pdf2image import convert_from_bytes
from PIL import Image
from zipfile import ZipFile

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'static/results'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/convert', methods=['POST'])
def convert_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # 고유 ID로 폴더 생성
    task_id = str(uuid.uuid4())
    task_folder = os.path.join(app.config['RESULT_FOLDER'], task_id)
    os.makedirs(task_folder, exist_ok=True)

    # PDF to JPG 변환
    images = convert_from_bytes(pdf_file.read(), dpi=200)
    image_urls = []

    for idx, img in enumerate(images):
        filename = f"page_{idx + 1}.jpg"
        path = os.path.join(task_folder, filename)
        img.save(path, 'JPEG')
        image_urls.append(f"/static/results/{task_id}/{filename}")

    # zip 파일 생성
    zip_path = os.path.join(task_folder, 'converted_images.zip')
    with ZipFile(zip_path, 'w') as zipf:
        for img_file in os.listdir(task_folder):
            if img_file.endswith('.jpg'):
                zipf.write(os.path.join(task_folder, img_file), img_file)

    zip_url = f"/static/results/{task_id}/converted_images.zip"

    return jsonify({
        'image_urls': image_urls,
        'zip_url': zip_url
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)