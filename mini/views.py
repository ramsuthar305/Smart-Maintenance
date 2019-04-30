from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request,'login.html')


def shome(request):
    return render(request,'student_home.html')

def whome(request):
    return render(request,'worker_home.html')

from django.http import HttpResponse
from .models import maintenance
from fastai import *
from fastai.vision import *


#classifier
def detect(request):
    lst=[]
    path=Path('last2/')
    classes=['garbage','pothole']
    np.random.seed(42)
    data = ImageDataBunch.from_folder(path, train=".", valid_pct=0.2,ds_tfms=get_transforms(), size=224, num_workers=0).normalize(imagenet_stats)
    learn = cnn_learner(data, models.resnet34, metrics=error_rate)
    learn.load('stage-1')
    learn.unfreeze()
    test_path=Path('static/')
    obj1=maintenance.objects.last()
    name=obj1.image.url
    nam=name
    nam=nam[7:]
    print('*'*10,nam,'*'*10)
    name='C:/Users/LENOVO/Documents/mini_project/'+name
    print('*'*50,name,'*'*50)
    test_image=open_image(name)
    for i in range(6):
        data2 = ImageDataBunch.single_from_classes(path, classes, ds_tfms=get_transforms(), size=240).normalize(imagenet_stats)
        learn = cnn_learner(data2, models.resnet34)
        pred_class,pred_idx,outputs = learn.predict(test_image)
        lst.append(pred_class)
    category=max(lst,key=lst.count)
    print('*\n'*5,category,'list=',lst,'\n*'*5)
    context={
        'category':category,
        'name':nam
    }
    return context
    #return render(request,'student_home.html',context)


# Create your views here.

def classify(request):
    return render(request,'student_home.html',{})

def image(request):
    if request.method=='POST' and request.FILES['img']:
        pic=request.FILES['img']
        obj=maintenance()
        obj.image=pic
        obj.save()
        context=detect(request)
        print("#*#"*10,context,"#*#"*10)
        return render(request,'student_home.html',context)

def camera(request):
    return render(request,'camera.html')

def loc(request):
    return render(request,'location.html')

def confirm(request):
    return render(request,'confirm.html')

def report(request):
    return render(request,'report.html')


def profile(request):
    return render(request,'profile.html')
