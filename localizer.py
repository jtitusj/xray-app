import os
os.environ["KERAS_BACKEND"] = "tensorflow"

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from keras.models import load_model
from PIL import Image
from vis import visualization

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
    prediction = model.predict(np.array([img_scaled]))[0]

    pred_idx = prediction.argmax()
    prob = prediction.max()
    label = labels[pred_idx]

    # create region of interest map
    layer_idx = len(model.layers) - 1
    cam = visualization.visualize_cam(model, layer_idx, pred_idx,
                                      np.array([img_scaled]))

    img_overlay = visualization.overlay(cam, img_resized, .3)

    return [label, prob, img_overlay]