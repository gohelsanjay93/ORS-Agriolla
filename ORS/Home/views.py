import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from Home.models import *
from adminside.models import CountryMaster, Statemaster, Citymaster

from Home.models import Category
from django.utils.crypto import get_random_string

from Home.models import Payment, Producttransaction
from .forms import *
from django.contrib import messages
from django.forms import forms


# Create your views here.
def home(request):
    Templates = "Home/index.html"
    if request.user.is_anonymous:
        changecountry = int(request.GET.get('country', 0))
        changestate = int(request.GET.get('state', 0))
        changecity = int(request.GET.get('city', 0))

        if changecountry == 0 and changestate == 0 and changecity == 0:
            if not request.session.has_key("city") and not request.session.has_key(
                    "state") and not request.session.has_key("city"):
                request.session['country'] = int(request.GET.get('country', random.choice([1, 2])))
                request.session['state'] = int(request.GET.get('state', random.choice([1, 2])))
                request.session['city'] = int(request.GET.get('city', random.choice([1, 2])))
                location = int(request.session['city'])
            else:
                location = int(request.session['city'])

        elif changecountry != 0 and changestate != 0 and changecity != 0:
            request.session['country'] = request.GET['country']
            request.session['state'] = request.GET['state']
            request.session['city'] = request.GET['city']
            location = request.session['city']

        elif changestate != 0 and changecity != 0:
            request.session['state'] = request.GET['state']
            request.session['city'] = request.GET['city']
            location = request.session['city']

        else:
            request.session['city'] = request.GET['city']
            location = request.session['city']

        items = Product.objects.filter(avail="Available", Owner_name__profile__city_id=location)
    else:
        change = int(request.GET.get('location', 0))
        if change != 0:
            location = change
        else:
            location = request.user.profile.city_id
        items = Product.objects.filter(avail="Available", Owner_name__profile__city_id=location)

    counts = {'tractors': 0, 'cultivator': 0, 'planting': 0, 'fertilizer': 0, 'irrigation': 0, 'harvestor': 0,
              'haymaker': 0, 'loading': 0, 'animalfood': 0, 'other': 0}
    for i in items:
        if i.category_id == 4:
            counts['tractors'] = counts['tractors'] + 1
        if i.category_id == 1:
            counts['cultivator'] = counts['cultivator'] + 1
        if i.category_id == 3:
            counts['planting'] = counts['planting'] + 1
        if i.category_id == 2:
            counts['fertilizer'] = counts['fertilizer'] + 1
        if i.category_id == 5:
            counts['irrigation'] = counts['irrigation'] + 1
        if i.category_id == 6:
            counts['harvestor'] = counts['harvestor'] + 1
        if i.category_id == 7:
            counts['haymaker'] = counts['haymaker'] + 1
        if i.category_id == 8:
            counts['loading'] = counts['loading'] + 1
        if i.category_id == 9:
            counts['animalfood'] = counts['animalfood'] + 1
        if i.category_id == 10:
            counts['other'] = counts['other'] + 1

    category = {"cultivator": 1,
                "fertilizer": 2,
                "planting": 3,
                "tractors": 4,
                "irrigation": 5,
                "harvestor": 6,
                "hay_maker": 7,
                "loading": 8,
                "animal_food": 9,
                "other": 10}
    return render(request, Templates,
                  {'items': items, 'category': category, 'count': counts, 'categories': Category.objects.all()})


@login_required(login_url='account_login')
def dashboard(request):
    items_list = Product.objects.filter(Owner_name=request.user)
    template = "dashboard.html"
    page = request.GET.get('page', 1)
    paginator = Paginator(items_list, 2)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    return render(request, template, {'items': items})


@login_required(login_url='account_login')
def addproduct(request):
    if request.method == 'POST':
        form = Productform(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'Added Product successfully..')
            return redirect("Home:home")
        else:
            messages.error(request, 'fill valid details')
    else:
        form = Productform()
    template = "ad-post.html"
    return render(request, template, {'form': form})


@login_required(login_url='account_login')
def editproduct(request, pk):
    template = "ad-post.html"
    items = get_object_or_404(Product, pk=pk)
    form = Productform(request.POST or None, request.FILES or None, instance=items)
    if form.is_valid():
        form.save()
        messages.success(request, "Items updated successfully...")
        return redirect("Home:home")
    return render(request, template, {"form": form})


@login_required(login_url='account_login')
def deleteproduct(request, pk):
    item = get_object_or_404(Product, pk=pk)
    item.delete()
    return redirect("Home:dashboard")


def aboutus(request):
    return render(request, "Home/about-us.html", {})


def contactus(request):
    if request.method == 'POST':
        form = Contactform(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            messages.success(request, 'Added Product successfully..')
            return redirect("Home:home")
        else:
            messages.error(request, 'fill valid details')
    else:
        form = Contactform()

    return render(request, "Home/contact-us.html", {'form': form})


@login_required(login_url='account_login')
def profile(request):
    if request.method == 'GET':
        template = "profile.html"
        return render(request, template, {'profile': Profile.objects.filter(user_id=request.user.id),
                                          'countries': CountryMaster.objects.all(), 'states': Statemaster.objects.all(),
                                          'cities': Citymaster.objects.all()})
    else:
        user = User.objects.get(id=request.user.id)
        user.first_name = request.POST['FirstName']
        user.last_name = request.POST['LastName']
        user.save()
        data = get_object_or_404(Profile, user_id=request.user.id)
        data.phone = request.POST['phone']
        data.address = request.POST['address']
        data.pincode = request.POST['pincode']
        data.country_id = request.POST['country']
        data.state_id = request.POST['state']
        data.city_id = request.POST['city']
        data.save()
        return redirect("Home:aboutme")


@login_required(login_url='account_login')
def saveprofile(request):
    if (request.POST):
        items = get_object_or_404(Profile, user_id=request.user.id)
        form = Profileform(request.POST, instance=items)
        if form.is_valid():
            form.save()
            return render(request, "profile.html", {'message': 'Success'})
    return render(request, "profile.html", {'Error': 'Something is Wrong', 'form': form})


@login_required(login_url='account_login')
def activead(request):
    activeaduser_list = Product.objects.filter(avail="Available", Owner_name=request.user)
    page = request.GET.get('page', 1)
    paginator = Paginator(activeaduser_list, 2)
    try:
        activeaduser = paginator.page(page)
    except PageNotAnInteger:
        activeaduser = paginator.page(1)
    except EmptyPage:
        activeaduser = paginator.page(paginator.num_pages)
    return render(request, "activeads.html", {'activead': activeaduser})


@login_required(login_url='account_login')
def pending(request):
    pendingads_list = Product.objects.filter(avail="!Available", Owner_name=request.user)
    page = request.GET.get('page', 1)
    paginator = Paginator(pendingads_list, 2)
    try:
        pendingads = paginator.page(page)
    except PageNotAnInteger:
        pendingads = paginator.page(1)
    except EmptyPage:
        pendingads = paginator.page(paginator.num_pages)
    return render(request, "pending-ads.html", {'pendingads': pendingads})


@login_required(login_url='account_login')
def aboutme(request):
    profile = get_object_or_404(Profile, user_id=request.user.id)
    activitystatus = Producttransaction.objects.get(borrower_id=request.user.id)
    # Activead=Product.objects.filter(avail="Available",Owner_name=request.user)
    Pendingads = Product.objects.filter(avail="!Available", Owner_name=request.user)
    return render(request, "Aboutme.html", {'prof': profile, 'pending': Pendingads,'purchase':activitystatus})


def AfterRegistration(request):
    return render(request, "account/verification_sent.html", {})


@login_required(login_url='account_login')
def paymentform(request, id):
    return render(request, 'Home/paymentform.html', {'data': Product.objects.get(id=id)})


@login_required(login_url='account_login')
def paymentdone(request):
    if request.method == 'POST':
        productinfo=Product.objects.get(id=request.POST['id'])

        newpayment =Payment.objects.create(transactionid=get_random_string(length=50),Merchant_id=productinfo.Owner_name_id,PaymentType=request.POST['type'],amount=request.POST['amount'],status=True,Paymentfor_id=productinfo.id
                                           )
        newpayment.save()
        newtransactionrecord=Producttransaction.objects.create(productid_id=productinfo.id,borrower_id=request.user.id,takendate=request.POST['from'],returndte=request.POST['to'])
        newtransactionrecord.save()

        productinfo.IsProductSoldOrOnRent=True
        productinfo.avail="!Available"
        productinfo.save()
        print("Payment done")
        return redirect("Home:home")
    return redirect("Home:payment", request.POST['id'])
