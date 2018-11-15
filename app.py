from flask import Flask, render_template, request, send_from_directory

import numpy as np
import pandas as pd
import json, os, base64, time, re, io

import matplotlib.image as mpimg
from PIL import Image
from io import BytesIO
from vis import visualization
from keras.models import load_model
import tensorflow as tf

app = Flask(__name__, static_url_path="", static_folder="")

global graph
graph = tf.get_default_graph() 
model_chexnet = load_model('bchou.hdf5')

@app.route('/')
def root():
    return send_from_directory('', 'index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    # process
    encoded_image = request.data
    encoded_image = re.findall(r'''(data:image\/\S+;base64,)(.+)''', encoded_image.decode('utf-8'))
    metadata = encoded_image[0][0]
    content = encoded_image[0][1]

    img = base64.b64decode(content)
    i = io.BytesIO(img)
    i = mpimg.imread(i, format='JPG')
    if len(i.shape)>2:
        i = i.mean(axis=2)
    
    label, prob, i = run(i, model_chexnet)
    print(label, prob)

    img = Image.fromarray(i)
    img = convertToPNG(img)

    return base64.b64encode(img)

def convertToPNG(im):
    with BytesIO() as f:
        im.save(f, format='PNG')
        return f.getvalue()

# resize image
def resize(img):
    img_ = img.resize((224, 224))
    
    # remove extra dimension for some images
    if len(img_.size) > 2:
        img_ = img_[:, :, 0]
        
    return np.asarray(np.dstack((img_, img_, img_)), dtype=np.uint8)

# transform image to fit model preprocessing
def transform_image(img):
    img_ = img / 255
    
    # standardize using imagenet mean and std
    imagenet_mean = np.array([0.485, 0.456, 0.406])
    imagenet_std = np.array([0.229, 0.224, 0.225])
    
    return (img_ - imagenet_mean) / imagenet_std

def run(input_img, model):
    # preprocess
    img = Image.fromarray(input_img)
    img_resized = resize(img)
    img_scaled = transform_image(img_resized)

    # labels
    labels = ['Atelectasis', 'Cardiomegaly', 'Effusion', 'Infiltration', 'Mass',
              'Nodule', 'Pneumonia', 'Pneumothorax', 'Consolidation', 'Edema',
              'Emphysema', 'Fibrosis', 'Pleural_Thickening', 'Hernia']

    # predict for image
    input_ = np.array([img_scaled])
    print(input_.shape)
    # prediction = model.predict(input_)[0]

    with graph.as_default():
        prediction = model.predict(input_)[0]

    pred_idx = prediction.argmax()
    prob = prediction.max()
    label = labels[pred_idx]

    # # create region of interest map
    layer_idx = len(model.layers) - 1
    with graph.as_default():
        cam = visualization.visualize_cam(model, layer_idx, pred_idx, np.array([img_scaled]))
        img_overlay = visualization.overlay(cam, img_resized, .3)

    return [label, prob, img_overlay]

if __name__ == '__main__':
    app.run(debug=True)
