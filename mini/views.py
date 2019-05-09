from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import STUDENT_REGISTER, WORKER_REGISTER1, REGISTRATIONS, LOGIN_DETAILS, ALL_PROBLEMS1, TEMP_PROBLEMS, TEMP_REPORT, WORKER_REPORT
from .models import maintenance
from fastai import *
from fastai.vision import *
import datetime
tempo = REGISTRATIONS.objects.all()
global var
info = {}
prob = {}
prob1 = {}
probid = 0
# Create your views here.
def login(request):
    global info
    if request.method=='POST':
        print("in login")
        data=request.POST
        em_id = data['email_id']
        ps = data['password']
        var = tempo.filter(email=em_id,password=ps)
        id=len(var)
        if id!=0:
            print(var[id-1].status)
            status= var[id-1].status
            login_details = LOGIN_DETAILS(email_id=data['email_id'],password=data['password'])
            login_details.save()
            if(id>0 and status=="available"):
                flag=1
                request.session["login"] = True
                request.session['u_id'] = var[0].user_id
                request.session['u_name'] = var[0].first_name
                request.session['u_email'] = var[0].email
                request.session['u_password'] = var[0].password
                print(request.session)
                if(request.session['u_email']==em_id and request.session['u_password']==ps):
                    info = {'user_id':request.session['u_id'], 'user_name':request.session['u_name'], 'email_id':request.session['u_email'], 'password':request.session['u_password']}

                if(var[0].user_name[3:5]=='ST'):
                    return redirect('/student_home/')

                if(var[0].user_name[3:5]=='WR'):
                    return redirect('/worker_home/')

    return render(request,'login.html')

def logout(request):
    global info
    info = {}
    request.session["user_name"] = False
    request.session["login"] = False
    return redirect('/login/')


def pro(request):
    context={}
    global info
    temp1 = info['email_id']
    print(temp1)
    var=tempo.filter(email=temp1)
    print(var)
    id=len(var)
    if id!=0:
        print("***")
        status=var[id-1].status
        if status=="available":
            first_name=var[id-1].first_name
            last_name=var[id-1].last_name
            institute =var[id-1].institute_name
            department=var[id-1].department
            email=var[id-1].email
            username=var[id-1].user_name
            password=var[id-1].password
            context['f_name']=first_name
            context['l_name']=last_name
            context['i_name']=institute
            context['d_name']=department
            context['e_mail']=email
            context['p_word']=password
            context['user_name']=username


        return render(request,"profile.html",context)
    return render(request,"profile.html",{})



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
        common = REGISTRATIONS(user_name=username,first_name=data['first_name'],last_name=data['last_name'],institute_name=data['institute_name'],department=data['department'],domain='NULL',email=data['email'],password=data['password'])
        common.save()
        context = {'display':"Registered Successfully"}
    return render(request,'student_register.html',context)

def worker_register(request):
    context = {}
    if request.method=='POST':
        print("in here")
        data = request.POST
        obj = WORKER_REGISTER1.objects.all()
        wcount = len(obj)
        username = "MITWR"+"00"+str(wcount+1)
        print(username)
        r = WORKER_REGISTER1(user_name=username,first_name=data['first_name'],last_name=data['last_name'],domain=data['domain'],email=data['email'],password=data['password'])
        r.save()
        common = REGISTRATIONS(user_name=username,first_name=data['first_name'],last_name=data['last_name'],institute_name='NULL',department='NULL',domain=data['domain'],email=data['email'],password=data['password'])
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
        #problem_type=detect(request)
        p = ALL_PROBLEMS1(description=prob['description'],location=prob['location'],image=prob['pic'],status=0,problem_type=detect(request),report_date=datetime.datetime.now().strftime("%d-%m-%Y"))
        p.save()
        print("confirm")
        return redirect("/student_home/")
    return render(request,'confirm.html',prob)




def block_id(request):
    if request.method == 'POST':
        data=request.POST
        print("*************************************")
        print(data)
        print("**************************************")
        some=data['username']
        print(some)
        var=tempo.filter(user_name=some)
        id=len(var)
        print("***")
        print(var[id-1].status)
        var[id-1].status="block"
        var[id-1].save()

    return render(request,"admin.html",{})

def block(request):
    return render(request,"block.html",{})

def unblock(request):
    return render(request,"unblock.html",{})

def unblock_id(request):
    if request.method == 'POST':
        data=request.POST
        print("*************************************")
        print(data)
        print("**************************************")
        some=data['username']
        print(some)
        var=tempo.filter(user_name=some)
        id=len(var)
        print("***")
        print(var[id-1].status)
        var[id-1].status="available"
        var[id-1].save()

    return render(request,"admin.html",{})


def rem(request):
    return render(request,"remove.html",{})

def rem_id(request):
    if request.method == 'POST':
        data=request.POST
        print("*************************************")
        print(data)
        print("**************************************")
        some=data['username']
        print(some)

        tempo.filter(user_name=some).delete()

    return render(request,"admin.html",{})

def profile(request):
    context={}
    if request.method == 'POST':
        data=request.POST
        print("*************************************")
        print(data)
        print("**************************************")
        some=data['username']
        print(some)

        var=tempo.filter(user_name=some)
        id=len(var)
        if id!=0:
            print("***")
            status=var[id-1].status
            if status=="available":
                first_name=var[id-1].first_name
                last_name=var[id-1].last_name
                institute =var[id-1].institute_name
                department=var[id-1].department
                email=var[id-1].email
                password=var[id-1].password
                context['f_name']=first_name
                context['l_name']=last_name
                context['i_name']=institute
                context['d_name']=department
                context['e_mail']=email
                context['p_word']=password
                context['user_name']=some

        return render(request,"profile.html",context)
    return render(request,"profile.html",{})

def s_change(request):
    if request.method == 'POST':
        data=request.POST
        print(data)
        some=data['user_id']
        l_name=data['l_name']
        user_name=data['user']
        email=data['email']
        password=data['password']
        var=tempo.filter(user_name=some)
        id=len(var)
        print("***")
        var[id-1].first_name=user_name
        var[id-1].last_name=l_name
        var[id-1].email=email
        var[id-1].password=password

        var[id-1].save()

        return redirect("/pro/")


def user_table(request):
    context={}
    temp=STUDENT_REGISTER.objects.all()
    context["student_data"]=temp
    return render(request,"user_table.html",context)


def worker_table(request):
    context={}
    temp=WORKER_REGISTER1.objects.all()
    context["worker_data"]=temp
    return render(request,"worker_table.html",context)

def garbage_table(request):
    context={}
    temp=ALL_PROBLEMS1.objects.filter(problem_type="Garbage")

    context["garbage_data"]=temp
    return render(request,"garbage_table.html",context)

def civil_table(request):
    context={}
    temp=ALL_PROBLEMS1.objects.filter(problem_type="Civil")

    context["civil_data"]=temp
    return render(request,"civil_table.html",context)

def all_problem_table(request):
    context={}
    temp=ALL_PROBLEMS1.objects.all()

    context["all_problem_data"]=temp
    return render(request,"all_problem_table.html",context)

def completed_table(request):
    context={}
    temp=ALL_PROBLEMS1.objects.filter(status="3")

    context["complete_data"]=temp
    return render(request,"completed_table.html",context)

def whome(request):
    global info
    global prob
    temp = ""
    temp1 = ""
    flag = 0
    pending = []

    if len(info)>0:
        print("info if")
        temp = info['user_name']
        obj123 = WORKER_REGISTER1.objects.filter(first_name=temp)
        if (len(obj123)>0):
            temp1 = obj123[0].domain
            print(obj123)
    p = ALL_PROBLEMS1.objects.all()
    for i in p:
        if i.status=='0' and i.problem_type==temp1:
            pending.append(i)

    worker_context = {'name':temp,'problems':pending}

    obj = ALL_PROBLEMS1.objects.filter(worker_name=temp)
    if(len(obj)>0):
        for i in obj:
            print(i.status)
            if i.status=='2':
                return render(request,'report.html')
            if i.status=='3':
                return render(request,'worker_home.html',worker_context)
    else:
        return render(request,'worker_home.html',worker_context)
    return render(request,'worker_home.html',worker_context)

def handle(request,problem_id):
    global info
    global probid
    temp = {}
    probid = problem_id
    status = 2
    p = ALL_PROBLEMS1.objects.get(pk=problem_id)
    p.status=status
    p.worker_name = info['user_name']
    p.save()
    print("in handle")
    print(problem_id)
    return render(request,"report.html")

def pass_pro(request):
    global info
    print("in pass")
    obj=ALL_PROBLEMS1.objects.get(worker_name=info['user_name'],status="2")

    obj.status=0
    obj.worker_name=""
    obj.save()
    return redirect("/worker_home/")

def wrong_domain(request,problem_id):
    global info
    global probid
    temp = {}
    temp1 = ""
    probid = problem_id
    p = ALL_PROBLEMS1.objects.get(pk=problem_id)
    if p.problem_type=="Garbage":
        temp1="Civil"
    if p.problem_type=="Civil":
        temp1="Garbage"
    p.problem_type=temp1
    p.save()
    print("in wrong domain")
    print(problem_id)
    return redirect("/worker_home/")


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

    #Uncomment the next statement to execute on Ram's Laptop
    name='C:/Users/LENOVO/Documents/mini_project/'+str(prob['pic'])

    #Uncomment the next statement to execute on Safir's Laptop
    #name='C:/Users/Admin/Documents/GitHub/smart-maintenance/'+str(prob['pic'])
    
    print('*'*50,name,'*'*50)
    test_image=open_image(name)
    for i in range(5):
        data2 = ImageDataBunch.single_from_classes(path, classes, ds_tfms=get_transforms(), size=240).normalize(imagenet_stats)
        learn = cnn_learner(data2, models.resnet34)
        pred_class,pred_idx,outputs = learn.predict(test_image)
        lst.append(pred_class)
    category=max(lst,key=lst.count)
    category=str(category)
    if category=="pothole":
        category="Civil"
    if category=="garbage":
        category="Garbage"
    print('*\n'*5,category,'list=',lst,'\n*'*5)
    return str(category)
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


def report(request):
    global info
    global prob1
    temp1 = ""
    if len(info)>0:
        temp1 = info['user_name']
    context = {'name':temp1}
    if request.method=="POST" and request.FILES['image']:
        pic=request.FILES['image']
        data=request.POST
        p = TEMP_REPORT(worker_name=temp1,description=data['description'],image=pic)
        p.save()
        print("saved worker report")
        temp = TEMP_REPORT.objects.all()
        l = len(temp)
        pic1 = temp[l-1].image
        print(pic1)
        prob1 = {'name':temp1,'description':data['description'],'pic':pic1}
        return redirect("/confirm1/")
    return render(request,'report.html',context)

def confirm1(request):
    global info
    global prob1

    if request.method=="POST":
        print(prob1['pic'])
        p = WORKER_REPORT(description=prob1['description'],image=prob1['pic'],date=datetime.datetime.now().strftime("%d-%m-%Y"))
        p.save()
        print("confirm")
        status = 3
        p = ALL_PROBLEMS1.objects.get(worker_name=info['user_name'],status=2)
        print(p.description)
        p.status=status
        p.completion_date=datetime.datetime.now().strftime("%d-%m-%Y")
        p.save()
        return redirect("/worker_home/")
    return render(request,'confirm1.html',prob1)

def edit(request):
    return render(request,'edit.htmL',{})


def worker_profile(request):
    return render(request,'worker_profile.html')

def admin(request):
    object=ALL_PROBLEMS1.objects.all()
    garbage=pothole=0
    complete_garbage=0
    incomplete_garbage=0
    complete_pothole=0
    incomplete_pothole=0
    date=''
    pdays=[]
    gdays=[]
    pd=[]
    gd=[]
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
        pd.append(pcount)
        gd.append(gcount)
        #pd[m]=pcount
        #gd[m]=gcount
        print("pd",m,": ",pd[m],"\n")
        print("gd",m,": ",gd[m],"\n")
        if m!=31:
            rang.append(m)
    print("pd----------------:",pd)
    print("gd----------------:",gd)
    print("total counts:\ngarbage:",garbage,"\npothole:",pothole)
    rangepdgd = zip(rang,pd,gd)
    context={
    'pothole':pothole,
    'garbage':garbage,
    'incomplete_pothole':incomplete_pothole,
    'complete_pothole':complete_pothole,
    'incomplete_garbage':incomplete_garbage,
    'complete_garbage':complete_garbage,
    'rangepdgd':rangepdgd,
    'rang':rang
    }
    return render(request,'admin.html',context)
