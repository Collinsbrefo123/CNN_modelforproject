import json

import tensorflow as tf
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from tensorflow import Graph
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from .models import CorridorLine,TowerName

tf.compat.v1.Session()

img_height, img_width = 80, 80



model = load_model('models/ConvolutionNeuralNetwork_v1.h5')


def homepage(request):
    return render(request, 'Convolution/homepage.html')



def homeconvo(request):
    return render(request, 'Convolution/homeconvo.html')


# for taking file to system is request.FILES
def predictImg(request):
    if request.method == 'GET':
        return render(request, 'Convolution/homeconvo.html')
    else:
        print(request.FILES.get('filePath'))
        file = request.FILES.get('filePath')
        print(file)
        fs = FileSystemStorage()
        filepath = fs.save(file.name, content=file)
        filepath = fs.url(filepath)
        testImage = '.' + filepath
        img = image.load_img(testImage, target_size=(img_height, img_width))
        x = image.img_to_array(img)
        x = x / 255
        x = x.reshape(1, img_height, img_width, 3)

        X = image.img_to_array(img)
        images = np.expand_dims(X, axis=0)
        val = model.predict(images)
        print(images)
        print(val)


        return render(request, 'Convolution/homeconvo.html', {'filePathName': val})



def loginpage(request):
    return render(request, 'Convolution/loginpage.html');


def transmission(request):
    return render(request, 'Convolution/home_trans.html')

def googlepage(request):
    Towers = TowerName.objects.all()
    print(Towers[0].towername)
    return render(request, 'Convolution/googlepage.html',{'Towers':Towers})
