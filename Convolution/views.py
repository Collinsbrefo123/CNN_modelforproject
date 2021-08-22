import tensorflow as tf
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .models import CorridorLine, TowerName, TowerImages
from tensorflow.keras.preprocessing import image
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
global graph,model
#initializing the graph
graph = tf.compat.v1.get_default_graph

print("Keras model loading.......")

model = load_model(r'C:\Users\kbref\Desktop\computer_vision\Convolutional_NN\Convolution\models\TestModel1.h5')
print('Model Loaded')


#creating a class dictionary
class_dict = {
    'House': 0,
    'Land': 1
}

class_names = list(class_dict.keys())


def homepage(request):
    return render(request, 'Convolution/homepage.html')


def homeconvo(request):
    Towers = TowerName.objects.all()
    print(Towers[0].towername)
    return render(request, 'Convolution/homeconvo.html', {'Towers': Towers})


# for taking file to system is request.FILES
def predictImg(request):
    return render(request, 'Convolution/homeconvo.html')



def loginpage(request):
    return render(request, 'Convolution/loginpage.html');


def transmission(request):
    return render(request, 'Convolution/home_trans.html')


def googlepage(request):
    Towers = TowerName.objects.all()
    print(Towers[0].towername)
    return render(request, 'Convolution/googlepage.html', {'Towers': Towers})


def detection(request):
    if request.method =='GET':
        Images = TowerImages.objects.all()
        print(Images[0].towerlocation)
        return render(request, 'Convolution/detection.html', {'imagesexample': Images[0].towerimage, 'TowerImages':Images})
    else:
        imagetower = request.POST.get('imagetower', False)
        # print(imagetower)
        Images = TowerImages.objects.all()
        Images1 = TowerImages.objects.filter(towerlocation=imagetower)
        # print(Images1)
        return render(request, 'Convolution/detection.html', {'imagesexample': Images1[0].towerimage, 'TowerImages':Images})

def modelprediction(request):
    if request.method == 'POST':
        myfile = request.FILES.get('imagetower')
        Images1 = TowerImages.objects.filter(towerlocation=myfile)

        # img = image.load_img(myfile)
        print(request)
        return render(request, 'Convolution/model.html')
    else:
        return redirect('detection')