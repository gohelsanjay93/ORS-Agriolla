from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.checks import messages
from django.http import JsonResponse, request
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.sessions.models import Session
from Home.models import Product

from Home.models import Profile

from Product.form import MachinereportForm

from Product.models import MachineReports
from .models import Employee, Workers


# Create your views here.
def choice(request):
    return render(request, "Choose/gateway.html", {})

def emplogin(request):
    if not request.session.has_key("emploggd"):
        return render(request, "Admin side/authentication/login.html", {})
    else:
        return redirect("Emp:index")

def validate_emp_username_login(request):
        user = request.POST.get('login', '')
        password = request.POST.get('password', '')
        taken = Employee.objects.filter(username__iexact=user).exists()
        both = Employee.objects.filter(username=user, password=password).exists()
        if user != '' and password != '':
            if taken:
                if both:
                    data = {'taken': True, 'pass': True, 'content': True}
                    Empname=get_object_or_404(Employee,username=user)
                    request.session["emploggd"]=True
                    request.session["emplogged"]=Empname.firstname
                    request.session["empid"] = Empname.id
                    #id and pass both right
                    return JsonResponse(data)
                    # return render(request,"Admin side/index.html", {})
                    # return redirect("Emp:index")
                else: #only password wrong
                    data = {'taken': True, 'pass': False, 'content': True, 'msg': 'plz enter valid password'}
                    return JsonResponse(data)
                    # return render(request, "Admin side/authentication/login.html", {'data':True,'v1':both,'v2':u,'v3':p,'v4':is_taken,'v5':user,'v6':password})

            else: #user not exist
                data = {'taken': False, 'pass': False, 'content': True, 'msg': 'plz enter valid username'}
                return JsonResponse(data)
                # return render(request, "Admin side/authentication/login.html", {'data':True,'v1':both,'v2':u,'v3':p,'v4':is_taken,'v5':user,'v6':password})

        else:
            data = {
                'content': False
            }

            return JsonResponse(data)


def index(request):
    if request.session.has_key('emploggd'):
        AllAds =Product.objects.all()
        Active=0
        Rented=0
        sell=0
        pending=0
        users=(User.objects.filter(is_active=1)).count()
        for i in AllAds:
            if i.avail == "Available":
                Active=Active+1
            if i.uploadfor == "Rent":
                Rented =Rented+1
            if i.uploadfor == "Sell":
                sell =sell+1
            if i.avail == "!Available" and i.verified_status == "no" and i.rejected_status=="no":
                pending=pending+1
        return render(request, "Admin side/index.html", {'live': Active, 'sell': sell, 'rent': Rented, 'pending': pending,'user':users})
    else:
        return redirect("Emp:emplogin")

def logout(request):
    if request.session.has_key("emploggd"):
        del request.session["emplogged"]
        del request.session["emploggd"]
        return redirect("Emp:emplogin")
    else:
        return redirect("Emp:emplogin")

def tables(request):
    if request.session.has_key("emploggd"):
        ads=Product.objects.all()
        return render(request,"Admin side/datatables.html",{'ads':ads})
    else:
        return redirect("Emp:emplogin")
def tablesuser(request):
    if request.session.has_key("emploggd"):
        userdata=User.objects.all()
        return render(request,"Admin side/users.html",{'user':userdata})
    else:
        return redirect("Emp:emplogin")
def view(request,id):
    if request.session.has_key("emploggd"):
        Ad=get_object_or_404(Product,id=id)

        userr=get_object_or_404(User,username=Ad.Owner_name)
        if(MachineReports.objects.filter(Adid_id=id)):
            form = MachinereportForm(instance=MachineReports.objects.get(Adid_id=id))
        else:
            form = MachinereportForm()
        profile=get_object_or_404(Profile,user_id=userr.id)
        return render(request,"Admin side/view.html",{'ad':Ad,'user':userr,'profile':profile,'workers':Workers.objects.filter(IsAvailable=True),'Form':form})
    else:
        return redirect("Emp:emplogin")
def SaveMachineReports(request):
    data=get_object_or_404(MachineReports,Adid_id=request.POST['ID'])
    data.ManufaturedDate=request.POST['ManufaturedDate']
    data.IdentificationNumber=request.POST['IdentificationNumber']
    data.Engine=request.POST['Engine']
    data.Power=request.POST['Power']
    data.Fuel=request.POST['Fuel']
    data.WorkEfficiency=request.POST['WorkEfficiency']
    data.IsWorking=request.POST['IsWorking']
    data.WorkFor1=request.POST['WorkFor1']
    data.WorkFor2=request.POST['WorkFor2']
    data.WorkFor3=request.POST['WorkFor3']
    data.Extrainfo = request.POST['Extrainfo']
    data.save()
    return redirect("Emp:view",request.POST['ID'])

def verified(request,id):
    if request.session.has_key("emploggd"):
        data=Product.objects.get(id=id)
        data.avail="Available"
        data.ApprovedOrRejectedBy_id=request.session['empid']
        data.save()
        return redirect("Emp:postreq")
    else:
        return redirect("Emp:emplogin")
def reject(request,id):
    if request.session.has_key("emploggd"):
        data=Product.objects.get(id=id)
        data.rejected_status="yes"
        data.ApprovedOrRejectedBy_id = request.session['empid']
        data.rejection_reason = request.POST['rejection_reason']
        data.save()
        return redirect("Emp:postreq")
    else:
        return redirect("Emp:emplogin")

def visitdate(request):
    if request.session.has_key("emploggd"):
        id = request.POST.get('adid', '')
        data=Product.objects.get(id=id)
        data.visit_date=request.POST.get('datetime', '')
        data.verifier_person_id=request.POST.get('person', '')
        data.save()
        return redirect("Emp:postreq")
    else:
        return redirect("Emp:emplogin")