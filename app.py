# taken from https://community.canvaslms.com/thread/2595

from flask import Flask, render_template,url_for, request, jsonify
import numpy as np
from PIL import Image
import re
import io
import base64
from PIL import Image, ImageEnhance, ImageFilter
import base64
from PIL import Image
import cv2
import pickle
import random

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])

def get_image(): 
    guess = 0
    print('3')
    if request.method== 'POST':
        #requests image from url 
        img_size = 56, 56 
        image_url = request.values['imageBase64']

        image_string = re.search(r'base64,(.*)', image_url).group(1)  

        #print(image_string)
        image_bytes = io.BytesIO(base64.b64decode(image_string))
        #print(image_bytes)

        image = Image.open(image_bytes) 
        image = image.resize(img_size, Image.LANCZOS)         
        image = image.convert('1')  
        image_array = np.asarray(image)
        data = Image.fromarray(image_array)
        data.save('gfg_dummy_pic2.png')
        image_array = image_array.flatten()

        image = cv2.imread('gfg_dummy_pic2.png')
        img = cv2.resize(image, (28,28))
        image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = (np.expand_dims(image,0))

        filename = 'handwriting_detector.pkl'
        model = pickle.load(open(filename, 'rb'))

        pred = model.predict(img).tolist()
        pred = pred[0]
        predicted_number = pred.index(max(pred))
        guess = predicted_number


        return jsonify(guess = guess) #returns as json format

    return render_template('index.html', guess = guess)

def numbers():
    li = [[] for i in range(10)]
    for i in range(10):
        for j in range(0,10-i):
            li[i].append(j)
    x = random.choice(li)
    y = random.choice(li[x])
    

    return render_template('index.html', number1=x, number2=y)



if __name__ == '__main__':
    app.run(debug = True)
