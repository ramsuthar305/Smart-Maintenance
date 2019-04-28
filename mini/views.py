from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request,'login.html')


def shome(request):
    return render(request,'student_home.html')

def whome(request):
    return render(request,'worker_home.html')
