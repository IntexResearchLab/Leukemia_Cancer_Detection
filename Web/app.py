from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import cv2
import numpy as np
from stardist.models import StarDist2D
from skimage.exposure import rescale_intensity
from keras.models import load_model
import os
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'tif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the pre-trained ensemble model
model = load_model('model/ensemble_model5')

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to preprocess image for classification
def preprocess_image(image):
    image = cv2.resize(image, (224, 224))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
    image /= 255.0
    return np.expand_dims(image, axis=0)

# Function to preprocess image for StarDist segmentation
def preprocess_for_stardist(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_purple = np.array([120, 50, 50])
    upper_purple = np.array([160, 255, 255])
    mask = cv2.inRange(hsv_image, lower_purple, upper_purple)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    opened_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opened_mask, kernel, iterations=3)
    return rescale_intensity(sure_bg, out_range=(0, 1))

# Function to apply segmentation and classification
def segment_and_classify_cells(image, model):
    preprocessed_image = preprocess_for_stardist(image)
    stardist_model = StarDist2D.from_pretrained('2D_versatile_fluo')
    labels, _ = stardist_model.predict_instances(preprocessed_image)
    
    result_image = image.copy()
    min_cell_area = 1500

    for label in np.unique(labels):
        if label == 0:
            continue
        mask = labels == label
        contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if cv2.contourArea(contour) < min_cell_area:
                continue
            cell_image = image[y:y+h, x:x+w]
            preprocessed_cell_image = preprocess_image(cell_image)
            predictions = model.predict(preprocessed_cell_image)
            cell_class = "Normal Cell" if predictions[0][0] > 0.5 else "Cancer Cell"
            color = (0, 0, 255) if cell_class == "Cancer Cell" else (0, 255, 0)
            cv2.rectangle(result_image, (x, y), (x + w, y + h), color, 2)
            cv2.putText(result_image, cell_class, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

    return result_image

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for the classification page (index.html)
@app.route('/classification', methods=['GET', 'POST'])
def classification():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Read and process the image
            image = cv2.imread(filepath)
            if image is None:
                return "Error: Could not read uploaded image", 400  # Handle invalid images
            
            classified_image = segment_and_classify_cells(image, model)

            # Save processed image in uploads folder
            output_filename = 'classified_' + filename
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            cv2.imwrite(output_path, classified_image)

            return render_template('index.html', original_image=filename, classified_image=output_filename)

    return render_template('index.html', original_image=None, classified_image=None)

# Route to serve processed image
@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Route for the About page (new route)
@app.route('/about')
def about():
    return render_template('about.html')


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
