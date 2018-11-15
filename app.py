from flask import Flask, render_template
from flask import send_from_directory
import pandas as pd
import json
import os
import base64

app = Flask(__name__, static_url_path='')


# df = pd.read_csv('census.csv')
# df.columns = ['province', 'city_muni', '1960', '1970', '1975', '1980', \
#             '1990', '1995', '2000', '2007', '2010', '2015']

@app.route('/')
def root():
    print('root!!')
    return send_from_directory('', 'index.html')
    # return app.send_static_file('/index.html')
    # return 'hi'

# @app.route('/census/latest')
# def get_latest():
#     filtered_df = df[['province', 'city_muni', '2015']]
#     # print(filtered_df)
#     return json.dumps(filtered_df.to_dict())

# @app.route('/census/<province>/<city>')
# def get_values_province_city(province, city):
#     filtered_df = df[(df['province'] == province) & (df['city_muni'] == city)]
#     return json.dumps(filtered_df.to_json(orient='split'))

@app.route('/process_image')
def process_image():
    # process
    success = True
    return str(success)

@app.route('/get_image1')
def get_image1():
    path = 'images/'
    filename = path+"neko_girl_1.jpg" 
    with open(filename, "rb") as f:
        data = f.read()
        encoded_image = base64.b64encode(data)
    return encoded_image

@app.route('/get_image2')
def get_image2():
    path = 'images/'
    filename = path+"anime_girl.png" 
    with open(filename, "rb") as f:
        data = f.read()
        encoded_image = base64.b64encode(data)
    return encoded_image 

# @app.route('/get_image')
# def get_image():
#     path = 'images'
#     files = ['neko_girl_1.jpg', 'anime_girl.png']
#     filenames = [path+"\\"+file for file in files]

#     encoded_images = {}
#     for key, filename in zip(['img1','img2'], filenames):
#         with open(filename, "rb") as f:
#             data = f.read()
#             encoded_image = base64.b64encode(data)
#         # print('done encoding image')
#         encoded_images[key] = encoded_image
#         print(encoded_images)
#     return json.dumps(encoded_images)
#     # return 'lala'
#     # return json.dumps({'lala': 1})

if __name__ == '__main__':
    app.run(debug=True)
