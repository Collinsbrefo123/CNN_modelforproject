import os
from django.shortcuts import render, redirect
from .models import CorridorLine, TowerName, TowerImages
import tensorflow as tf
from .my_models import ai_model

global graph, model
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from twilio.rest import Client

# initializing the graph
graph = tf.compat.v1.get_default_graph

global myimage
myimage = None


def homepage(request):
    return render(request, 'Convolution/homepage.html')

@login_required
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

@login_required
def logoutpage(request):
    if request.method == 'POST':
        logout(request)
        return redirect('loginpage')

@login_required
def transmission(request):
    return render(request, 'Convolution/home_trans.html')

@login_required
def googlepage(request):
    Towers = TowerName.objects.all()
    print(Towers[0].towername)
    return render(request, 'Convolution/googlepage.html', {'Towers': Towers})

@login_required
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

@login_required
def modelprediction(request):
    if request.method == 'POST':
        print(request.POST.get('text'))
        print(request.POST.get('towerimages'))
        name = request.POST.get('towerimages')
        towername = request.POST.get('towername')

        filename_basepath = os.path.basename(name)
        ai_model.crop_one_picture(filename=filename_basepath)
        result = ai_model.Model_Predictions()
        filename_save = os.path.splitext(filename_basepath)[0]
        savename = ai_model.merge_picture(filename_save)

        if savename:
            print("There are approximately ", len(result), " anomalies detected")
            print("The saved name is", savename)
            ai_model.delete_files()
            return render(request, 'Convolution/model.html', {"towername":towername, "image": savename,"image_name":filename_save, "result_length": len(result)})
    else:
        return redirect('detection')

@login_required
def notification(request):
    if request.method == "POST":
        anomalies = request.POST.get('tower_anomalies')
        towernames = request.POST.get('towernames')
        # account_sid = 'AC8b068955f979e2a9d40b000db50fdbe3'
        # auth_token = 'd18660734a845d27f7753656c8373ba5'
        # # account_sid = os.environ['AC8b068955f979e2a9d40b000db50fdbe3']
        # # auth_token = os.environ['c757543d0dfe7bb2f423b22848d98d10']
        # client = Client(account_sid, auth_token)
        #
        # message = client.messages.create(
        #     body='There are some anomalies detected',
        #     from_='+19842046149',
        #     to='+233579418353'
        # )
        account_sid = 'AC8b068955f979e2a9d40b000db50fdbe3'
        auth_token = 'd18660734a845d27f7753656c8373ba5'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            #SMS notification
            # body='There are '+ anomalies +' anomalies detected',
            # from_='+19842046149',
            # to='++233202450312'
            #whatsapp notification
            from_='whatsapp:+14155238886',
            body='There are '+ anomalies +' anomalies detected at '+str(towernames),
            to='whatsapp:+233579418353'
        )

        print(message.sid)

        print(message.body)

        return render(request, 'Convolution/notify.html', {'message': 'Notification Sent', 'anomalies': anomalies, 'message':message.sid})
