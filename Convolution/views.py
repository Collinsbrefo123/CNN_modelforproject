import os

import tensorflow as tf
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from .models import CorridorLine, TowerName, TowerImages
from tensorflow.keras.preprocessing import image
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from .my_models import ai_model
global graph,model
#initializing the graph
graph = tf.compat.v1.get_default_graph

print("Keras model loading.......")



global myimage
myimage = None

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
        return render(request, 'Convolution/detection.html', {'imagesexample': Images[0].towerimage, 'TowerImages':Images})
    else:
        imagetower = request.POST.get('imagetower', False)
        global myimage
        # print(imagetower)
        Images = TowerImages.objects.all()
        Images1 = TowerImages.objects.filter(towerlocation=imagetower)
        myimage = Images1[0].towerimage
        # print(Images1)
        return render(request, 'Convolution/detection.html', {'imagesexample': Images1[0].towerimage, 'TowerImages':Images})

def modelprediction(request):
    if request.method == 'POST':
        global myimage
        print(request.POST.get('text'))
        print(request.POST.get('towerimages'))
        name =request.POST.get('towerimages')
        filename_basepath=os.path.basename(name)
        ai_model.crop_one_picture(filename=filename_basepath)
        result=ai_model.Model_Predictions()
        filename_save = os.path.splitext(filename_basepath)[0]
        savename=ai_model.merge_picture(filename_save)

        if savename:
            print("There are approximately ", len(result), " anomalies detected")
            print("The saved name is", savename)
            # ai_model.delete_files()


        return render(request, 'Convolution/model.html',{"image":savename, "result_length":len(result)})
    else:
        return redirect('detection')