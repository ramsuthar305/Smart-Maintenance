from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import REGISTER, LOGIN_DETAILS, PROBLEMS, TEMP_PROBLEMS

info = {}
prob={}
# Create your views here.
def login(request):
    global info
    if request.method=='POST':
        print("in login")
        data=request.POST
        em_id = data['email_id']
        ps = data['password']
        r = REGISTER.objects.filter(email=em_id,password=ps)
        print(r)
        login_details = LOGIN_DETAILS(email_id=data['email_id'],password=data['password'])
        login_details.save()
        if(len(r)>0):
            flag=1
            request.session["login"] = True
            request.session['u_id'] = r[0].user_id
            request.session['u_name'] = r[0].first_name
            request.session['u_email'] = r[0].email
            request.session['u_password'] = r[0].password
            print(request.session)
            if(request.session['u_email']==em_id and request.session['u_password']==ps):
                info = {'user_id':request.session['u_id'], 'user_name':request.session['u_name'], 'email_id':request.session['u_email'], 'password':request.session['u_password']}

        return redirect('/student_home/')

    return render(request,'login.html')

def logout(request):
    global info
    info = {}
    request.session["user_name"] = False
    request.session["login"] = False
    return redirect('/login/')

def register(request):
    context = {}
    if request.method=='POST':
        print("in here")
        data = request.POST
        r = REGISTER(first_name=data['first_name'],last_name=data['last_name'],institute_name=data['institute_name'],department=data['department'],email=data['email'],password=data['password'])
        r.save()
        context = {'display':"Registered Successfully"}
    return render(request,'register.html',context)


def shome(request):
    global info
    global prob
    temp = ""
    if len(info)>0:
        temp = info['user_name']
    context = {'name':temp}
    if request.method=="POST" and request.FILES['image']:
        pic=request.FILES['image']
        data=request.POST
        p = TEMP_PROBLEMS(description=data['description'],location=data['location'],image=pic)
        p.save()
        print("saved student problem")
        temp = TEMP_PROBLEMS.objects.all()
        l = len(temp)
        pic1 = temp[l-1].image
        print(pic1)
        prob = {'description':data['description'],'location':data['location'],'pic':pic1}
        return redirect("/confirm/")


    return render(request,'student_home.html',context)

def confirm(request):
    global prob
    if request.method=="POST":
        p = PROBLEMS(description=prob['description'],location=prob['location'],image=prob['pic'])
        p.save()
        print("confirm")
        return redirect("/student_home/")
    return render(request,'confirm.html',prob)




def whome(request):
    p = PROBLEMS.objects.all()
    worker_context = {'problems':p}
    print(p)
    return render(request,'worker_home.html',worker_context)





from django.http import HttpResponse
from .models import maintenance
#from fastai import *
#from fastai.vision import *

'''
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
'''
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


def report(request):
    return render(request,'report.html')


def profile(request):
    return render(request,'profile.html')

def worker_profile(request):
    return render(request,'worker_profile.html')

def admin(request):
    return render(request,'admin.html')
