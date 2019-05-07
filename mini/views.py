from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import STUDENT_REGISTER, WORKER_REGISTER, REGISTRATIONS, LOGIN_DETAILS, ALL_PROBLEMS, TEMP_PROBLEMS
from django.http import HttpResponse
from .models import maintenance
from fastai import *
from fastai.vision import *
import datetime

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
        r = REGISTRATIONS.objects.filter(email=em_id,password=ps)
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

            if(r[0].user_name[3:5]=='ST'):
                return redirect('/student_home/')

            if(r[0].user_name[3:5]=='WR'):
                return redirect('/worker_home/')

    return render(request,'login.html')

def logout(request):
    global info
    info = {}
    request.session["user_name"] = False
    request.session["login"] = False
    return redirect('/login/')

def student_register(request):
    context = {}
    if request.method=='POST':
        print("in here")
        data = request.POST
        obj = STUDENT_REGISTER.objects.all()
        scount = len(obj)
        username = "MITST"+"00"+str(scount+1)
        r = STUDENT_REGISTER(user_name=username,first_name=data['first_name'],last_name=data['last_name'],institute_name=data['institute_name'],department=data['department'],email=data['email'],password=data['password'])
        r.save()
        common = REGISTRATIONS(user_name=username,first_name=data['first_name'],last_name=data['last_name'],institute_name=data['institute_name'],department=data['department'],email=data['email'],password=data['password'])
        common.save()
        context = {'display':"Registered Successfully"}
    return render(request,'student_register.html',context)

def worker_register(request):
    context = {}
    if request.method=='POST':
        print("in here")
        data = request.POST
        obj = WORKER_REGISTER.objects.all()
        wcount = len(obj)
        username = "MITWR"+"00"+str(wcount+1)
        r = WORKER_REGISTER(user_name=username,first_name=data['first_name'],last_name=data['last_name'],institute_name=data['institute_name'],department=data['department'],email=data['email'],password=data['password'])
        r.save()
        common = REGISTRATIONS(user_name=username,first_name=data['first_name'],last_name=data['last_name'],institute_name=data['institute_name'],department=data['department'],email=data['email'],password=data['password'])
        common.save()
        context = {'display':"Registered Successfully"}
    return render(request,'worker_register.html',context)

def shome(request):
    global info
    global prob
    temp1 = ""
    if len(info)>0:
        temp1 = info['user_name']
    context = {'name':temp1}
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
        prob = {'name':temp1,'description':data['description'],'location':data['location'],'pic':pic1}
        return redirect("/confirm/")
    return render(request,'student_home.html',context)

def confirm(request):
    global info
    global prob

    if request.method=="POST":
        print(prob['pic'])
        p = ALL_PROBLEMS(description=prob['description'],location=prob['location'],image=prob['pic'],status=0,problem_type=detect(request),date=datetime.datetime.now().strftime("%d-%m-%Y"))
        p.save()
        print("confirm")
        return redirect("/student_home/")
    return render(request,'confirm.html',prob)




def whome(request):
    global info
    global prob
    temp = ""
    flag = 0
    pending = []
    if len(info)>0:
        temp = info['user_name']
    p = ALL_PROBLEMS.objects.all()
    for i in p:
        if i.status=='0':
            pending.append(i)
    worker_context = {'name':temp,'problems':pending}

    obj = ALL_PROBLEMS.objects.filter(worker_name=temp)
    if(len(obj)>0):
        for i in obj:
            print(i.status)
            if i.status=='2':
                return render(request,'report.html')
    else:
        return render(request,'worker_home.html',worker_context)

def handle(request,problem_id):
    global info
    temp = {}
    status = 2
    p = ALL_PROBLEMS.objects.get(pk=problem_id)
    p.status=status
    p.worker_name = info['user_name']
    p.save()
    print("in handle")
    print(problem_id)
    return render(request,"report.html")

def pass_prob(request,problem_id):
    print("in pass")
    print(problem_id)
    return HttpResponse("DONE")






#classifier
def detect(request):
    global prob
    print(str(prob['pic']))
    lst=[]
    path=Path('last2/')
    classes=['garbage','pothole']
    np.random.seed(42)
    data = ImageDataBunch.from_folder(path, train=".", valid_pct=0.2,ds_tfms=get_transforms(), size=224, num_workers=0).normalize(imagenet_stats)
    learn = cnn_learner(data, models.resnet34, metrics=error_rate)
    learn.load('stage-1')
    learn.unfreeze()
    test_path=Path('static/')
    #obj1=maintenance.objects.last()
    #name=obj1.image.url
    #nam=name
    #nam=nam[7:]
    #print('*'*10,nam,'*'*10)
    name='C:/Users/LENOVO/Documents/mini_project/'+str(prob['pic'])
    print('*'*50,name,'*'*50)
    test_image=open_image(name)
    for i in range(5):
        data2 = ImageDataBunch.single_from_classes(path, classes, ds_tfms=get_transforms(), size=240).normalize(imagenet_stats)
        learn = cnn_learner(data2, models.resnet34)
        pred_class,pred_idx,outputs = learn.predict(test_image)
        lst.append(pred_class)
    category=max(lst,key=lst.count)
    print('*\n'*5,category,'list=',lst,'\n*'*5)
    return str(category)
    #return render(request,'student_home.html',context)

'''
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
    object=ALL_PROBLEMS.objects.all()
    garbage=pothole=0
    complete_garbage=0
    incomplete_garbage=0
    complete_pothole=0
    incomplete_pothole=0
    date=''
    pdays=[]
    gdays=[]
    pd={}
    gd={}
    gcount=pcount=0
    rang=[]
    for i in object:
        print("0"*5,i.problem_type)
        if i.problem_type=="pothole":
            pothole+=1
            if i.status=="0":
                incomplete_pothole+=1
            if i.status=="1":
                complete_pothole+=1
            date=datetime.datetime.now().strftime("%m")
            if date==i.date[3:5]:
                pdays.append(int(i.date[0:2]))
            print("civil problem detected")

        if i.problem_type=="garbage":
            garbage+=1
            if i.status=="0":
                incomplete_garbage+=1
            if i.status=="1":
                complete_garbage+=1
            if date==i.date[3:5]:
                gdays.append(int(i.date[0:2]))
            print("garbage problem detected")
    for m in range(31):
        pcount=pdays.count(m)
        gcount=gdays.count(m)
        pd[m]=pcount
        gd[m]=gcount
        print("pd",m,": ",pd[m],"\n")
        print("gd",m,": ",gd[m],"\n")    
        if m!=31:
            rang.append(m)
    print("pd----------------:",pd)
    print("gd----------------:",gd)
    print("total counts:\ngarbage:",garbage,"\npothole:",pothole)
    context={
    'pothole':pothole,
    'garbage':garbage,
    'incomplete_pothole':incomplete_pothole,
    'complete_pothole':complete_pothole,
    'incomplete_garbage':incomplete_garbage,
    'complete_garbage':complete_garbage,
    'pd':pd,
    'gd':gd,
    'rang':rang
    }
    return render(request,'admin.html',context)
