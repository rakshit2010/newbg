# app.py
import os
from flask import Flask, render_template, request
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/results'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    result_image = None
    if request.method == 'POST':
        uploaded_file = request.files['image']
        input_bytes = uploaded_file.read()
        result_bytes = remove(input_bytes)
        result_img = Image.open(io.BytesIO(result_bytes))
        # Save edited image to static folder for display
        output_filename = f"result_{uploaded_file.filename}"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        output_filename = f"result_{os.path.splitext(uploaded_file.filename)}.png"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        result_img.save(output_path, format='PNG')

        result_image = output_filename
    return render_template('index.html', result_image=result_image)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    app.run(debug=True)

