from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
import requests
# Create your views here.
def index(request):
    return render(request,'index.html')
def service(request):
    return render(request,'service.html')
def project(request):
    return render(request,'project.html')
def about(request):
    return render(request,'about.html')
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        message = request.POST.get('message')
        enq = Enquiry(name = name, contactno = contactno, email = email, subject = subject, message = message)
        enq.save()
        url = "http://sms.bulkssms.com/submitsms.jsp"
        params = {
            "user": "BRIJESH",
            "key": "066c862acdXX",
            "mobile": f"{contactno}",
            "message": "Thanks for enquiry we will contact you soon.\n\n-Bulk SMS",
            "senderid": "UPDSMS",
            "accusage": "1",
            "entityid": "1201159543060917386",
            "tempid": "1207169476099469445"
        }
        response = requests.get(url, params=params)
        print("Response:", response.text)
        messages.success(request, "Your enquiry has been submited succesfully")
        return redirect('contact')
    return render(request,'contact.html')
def sign(request):
    return render(request,'sign.html')


def signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        contactno = request.POST.get('contactno')
        usertype = request.POST.get('usertype')
        password = request.POST.get('password')
        u = LoginInfo.objects.filter(username=email)
        if u:
            messages.error(request,"Email already exists")
            return redirect('signup')
        log = LoginInfo(usertype=usertype,username=email,password=password)
        user = UserInfo(name=name,email=email,contactno=contactno,login=log)
        log.save()
        user.save()
        messages.success(request,"You are registerd")
    return render(request,'signup.html')

def sign(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            log = LoginInfo.objects.get(username=username,password=password)
            if log is not None:
                if log.usertype.lower() == "homeowner":
                    request.session['homeownerid'] = username
                    messages.success(request," welcome homeowner")
                    return redirect('homeownerdash')
                elif log.usertype.lower() == "contractor":
                    request.session['contractorid'] = username
                    messages.success(request,'Welcome Contractor')
                    return redirect('contractordash')
                else:
                    messages.error(request,"somthing went wrong")
                    return redirect('sign')
        except LoginInfo.DoesNotExist:
            messages.error(request,"Invalid username or password") 
            return redirect('sign')
    return render(request,'sign.html')        

def self(request):
    return render(request,'self.html')
def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            ad = LoginInfo.objects.get(username=username,password=password ,usertype="admin")
            if ad is not None:
                request.session['adminid'] = username
                messages.success(request,"Welecome Admin")
                return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request,"Invalid username or password")
            return redirect('adminlogin')
    return render(request,'adminlogin.html')

