from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import*
from homeownerapp.models import *
from contractorapp.models import *
from django.views.decorators.cache import cache_control

# Create your views here. 
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def admindash(request):
    if not 'adminid'in request.session:
        messages.error(request,"you are not logged in")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    context = {
        'adminid':adminid,
        'th': UserInfo.objects.filter(login__usertype="homeowner").count(),
        'tc': UserInfo.objects.filter(login__usertype="contractor").count(),
        'tp': Project.objects.all().count(),
        'trp': Project.objects.filter(status="under_construction").count(),
        'tcp': Project.objects.filter(status="completed").count(),
        'enq': Enquiry.objects.all().count(),

        




    }
    return render(request,'admindash.html',context)

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def adminlogout(request):
    if 'adminid' in request.session:
        del request.session ['adminid']
        messages.success(request,"you are logged out")
        return redirect('adminlogin')
    else:
        return redirect('index')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)    
def viewenq(request):
    if not 'adminid'in request.session:
        messages.error(request,"you are not logged in")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    enqs =Enquiry.objects.all()
    return render(request,'viewenq.html',{'enqs':enqs ,'adminid':adminid})
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def delenq(request, id):
    if not 'adminid'in request.session:
        messages.error(request,"you are not logged in")
        return redirect('adminlogin')
    enq =Enquiry.objects.get(id =id )
    enq.delete()
    messages.success(request,"Enquriy deleted succesfully")
    return redirect('viewenq')

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def change(request):
    if not 'adminid'in request.session:
        messages.error(request,"you are not logged in")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    if request.method  == 'POST':
            oldpwd = request.POST.get('oldpwd')
            newpwd = request.POST.get('newpwd') 
            confirmpwd = request.POST.get('confirmpwd')
            try:
                admin = LoginInfo.objects.get(username = adminid)
                if admin.password != oldpwd:
                    messages.error(request, "old password is incorrect")
                    return redirect('change')
                elif newpwd != confirmpwd:
                    messages.error (request,"New password and confirm did not match")
                    return redirect('change')
                elif admin.password == newpwd:
                    messages.error(request,"New password is same as a old password")
                    return redirect('change')
                else:
                    admin.password = newpwd
                    admin.save()
                    messages.success(request,"Password changed succesfully")
                    return redirect('admindash')
            except LoginInfo.DoesNotExist:
                messages.error(request,"Something went wrong") 
                return redirect('adminlogin')   
    return render(request,'change.html',{'adminid':adminid})


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def managecontractors(request): 
    if not 'adminid'in request.session:
        messages.error(request,"you are not logged in")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    contractors = UserInfo.objects.filter(login__usertype = 'contractor')
    return render(request,'managecontractors.html',{'adminid':adminid,'contractors':contractors})


@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def managehomeowners(request):
    if not 'adminid'in request.session:
        messages.error(request,"you are not logged in")
        return redirect('adminlogin')
    adminid = request.session.get('adminid')
    homeowners = UserInfo.objects.filter(login__usertype = 'homeowner')
    return render(request,'managehomeowners.html',{'adminid':adminid,'homeowners':homeowners})
