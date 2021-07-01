import json

import tensorflow as tf
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from tensorflow import Graph
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

tf.compat.v1.Session()

img_height, img_width = 100, 100
with open('models/imagenet_classes.json', 'r') as f:
    labelInfo = f.read()

labelInfo = json.loads(labelInfo)

model_graph = Graph()
with model_graph.as_default():
    tf_session = tf.compat.v1.Session()
    with tf_session.as_default():
        model = load_model('models/ConvolutionNeuralNetwork_v1.h5')


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
        filepathname = fs.save(file.name, content=file)
        filepathname = fs.url(filepathname)
        testImage = '.' + filepathname
        img = image.load_img(testImage, target_size=(img_height, img_width))
        x = image.img_to_array(img)
        x = x / 255
        x = x.reshape(1, img_height, img_width, 3)
        with model_graph.as_default():
            with tf_session.as_default():
                predi = model.predict(x)
                print(predi)

        import numpy as np
        predictedLabel = labelInfo[str(np.argmax(predi[0]))]

        return render(request, 'Convolution/homeconvo.html', {'filePathName': filepathname, 'predictedLabel': predictedLabel})



def loginpage(request):
    return render(request, 'Convolution/loginpage.html');


def transmission(request):
    return render(request, 'Convolution/home_trans.html')

def googlepage(request):
    return render(request, 'Convolution/googlepage.html')
