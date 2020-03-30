from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from adminside.models import Workers

from Home.models import Product

from Home.models import Profile

from Product.form import MachinereportForm

from Product.models import MachineReports


def Worker_login(request):
    if not request.session.has_key("workersession"):
        return render(request, "Worker/authentication/login.html", {})
    else:
        return redirect("Worker:index")

def validate_worker_username_login(request):
    user = request.POST.get('login', '')
    password = request.POST.get('password', '')
    taken = Workers.objects.filter(Username__iexact=user).exists()
    both = Workers.objects.filter(Username=user, Password=password).exists()
    if user != '' and password != '':
        if taken:
            if both:
                data = {'taken': True, 'pass':True,'content': True}
                Worker = get_object_or_404(Workers, Username=user)
                request.session["workersession"] = Worker.FirstName
                request.session["id"] = Worker.id
                Worker.IsAvailable=True
                Worker.save()
                return JsonResponse(data)
            else:
                data = {'taken': True, 'pass': False, 'content': True, 'msg': 'plz enter valid password'}
                return JsonResponse(data)
        else:
            data = {'taken': False, 'pass': False, 'content': True, 'msg': 'plz enter valid username'}
            return JsonResponse(data)
    else:
        data = {
            'content': False
        }
    return JsonResponse(data)

def index(request):
    if request.session.has_key('workersession'):
        data=Product.objects.filter(verifier_person_id=request.session["id"],IsVisited=False)

        page = request.GET.get('page', 1)
        paginator = Paginator(data, 2)
        try:
            datalist = paginator.page(page)
        except PageNotAnInteger:
            datalist = paginator.page(1)
        except EmptyPage:
            datalist = paginator.page(paginator.num_pages)
            datalist =datalist

        return render(request, "Worker/index.html", {'data':datalist})
    else:
        return redirect("Worker:worker")

def logout(request):
    if request.session.has_key('workersession'):
        Worker = get_object_or_404(Workers,id=request.session['id'])
        Worker.IsAvailable=False
        Worker.save()
        del request.session["workersession"]
        return redirect("Worker:worker")
    else:
        return redirect("Worker:worker")

def addetails(request,id):
    if request.session.has_key('workersession'):
        data=get_object_or_404(Product,id=id)
        Owner=get_object_or_404(Profile,user_id=data.Owner_name_id)
        return render(request,"Worker/details.html",{'data':data,'userdata':Owner,'Form':MachinereportForm()})
    else:
        return redirect("Worker:worker")

def savereport(request):
    if request.session.has_key('workersession'):
        if(request.method == "POST"):
            data=MachineReports.objects.create(Adid_id=request.POST['ID'],ManufaturedDate=request.POST['ManufaturedDate'],IdentificationNumber=request.POST['IdentificationNumber'],Engine=request.POST['Engine'],Power=request.POST['Power'],Fuel=request.POST['Fuel'],WorkEfficiency=request.POST['WorkEfficiency'],IsWorking=request.POST['IsWorking'],WorkFor1=request.POST['WorkFor1'],WorkFor2=request.POST['WorkFor2'],WorkFor3=request.POST['WorkFor3'])
            data.save()

            visit =get_object_or_404(Product,id=request.POST['ID'])
            visit.IsVisited=True
            visit.verifed_status="yes"
            visit.save()
            return redirect("Worker:addetails",request.POST['ID'])
        return redirect("Worker:addetails",request.POST['ID'])
    else:
        return redirect("Worker:worker")
