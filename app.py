from flask import Flask, render_template, request, send_from_directory

import pandas as pd
import json, os, base64, time, re, io
import matplotlib.image as mpimg


app = Flask(__name__, static_url_path="", static_folder="")

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

    # img = base64.b64decode(content)
    # i = io.BytesIO(img)
    # i = mpimg.imread(i, format='JPG')

    # print(i)
    # print(type(request.data))

    return (metadata+content).encode()


# @app.route('/get_image1')
# def get_image1():
#     path = 'images/'
#     filename = path+"neko_girl_1.jpg" 
#     with open(filename, "rb") as f:
#         data = f.read()
#         encoded_image = base64.b64encode(data)
#     return encoded_image

# @app.route('/get_image2')
# def get_image2():
#     time.sleep(2)
#     path = 'images/'
#     filename = path+"anime_girl.png" 
#     with open(filename, "rb") as f:
#         data = f.read()
#         encoded_image = base64.b64encode(data)
#     return encoded_image 

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
