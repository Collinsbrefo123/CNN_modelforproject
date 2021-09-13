import os
from django.shortcuts import render, redirect
from .models import CorridorLine, TowerName, TowerImages
import tensorflow as tf
from .my_models import ai_model

global graph, model
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from twilio.rest import Client

# initializing the graph
graph = tf.compat.v1.get_default_graph

global myimage
myimage = None


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
    if request.method == 'GET':
        return render(request, 'Convolution/loginpage.html');
    else:
        username = request.POST.get('username', False)
        password = request.POST.get('pass', False)
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'Convolution/loginpage.html', {'error': 'Wrong User details'})
        else:
            login(request, user)
            return redirect('transmission')


def logoutpage(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginpage')


def transmission(request):
    return render(request, 'Convolution/home_trans.html')


def googlepage(request):
    Towers = TowerName.objects.all()
    print(Towers[0].towername)
    return render(request, 'Convolution/googlepage.html', {'Towers': Towers})


def detection(request):
    if request.method == 'GET':
        Images = TowerImages.objects.all()
        return render(request, 'Convolution/detection.html',
                      {'imagesexample': Images[0].towerimage, 'TowerImages': Images})
    else:
        imagetower = request.POST.get('imagetower', False)
        global myimage
        # print(imagetower)
        Images = TowerImages.objects.all()
        Images1 = TowerImages.objects.filter(towerlocation=imagetower)
        print(Images1[0])
        return render(request, 'Convolution/detection.html',
                      {'imagesexample': Images1[0].towerimage, 'imagename': Images1[0], 'TowerImages': Images})


def modelprediction(request):
    if request.method == 'POST':
        print(request.POST.get('text'))
        print(request.POST.get('towerimages'))
        name = request.POST.get('towerimages')
        filename_basepath = os.path.basename(name)
        ai_model.crop_one_picture(filename=filename_basepath)
        result = ai_model.Model_Predictions()
        filename_save = os.path.splitext(filename_basepath)[0]
        savename = ai_model.merge_picture(filename_save)

        if savename:
            print("There are approximately ", len(result), " anomalies detected")
            print("The saved name is", savename)
            # ai_model.delete_files()
            return render(request, 'Convolution/model.html', {"image": savename, "result_length": len(result)})
    else:
        return redirect('detection')


def notification(request):
    if request.method == "POST":
        account_sid = 'AC8b068955f979e2a9d40b000db50fdbe3'
        auth_token = 'c757543d0dfe7bb2f423b22848d98d10'
        # account_sid = os.environ['AC8b068955f979e2a9d40b000db50fdbe3']
        # auth_token = os.environ['c757543d0dfe7bb2f423b22848d98d10']
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body='There are some anomalies detected',
            from_='+19842046149',
            to='+233202450312'
        )

        print(message.sid)
        anomalies = request.POST.get('tower_anomalies')
        return render(request, 'Convolution/notify.html', {'message': 'Notification Sent', 'anomalies': anomalies})
