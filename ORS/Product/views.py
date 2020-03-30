import random

from django.core import paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.
from Home.models import Product

from Home.models import Profile

from Product.models import MachineReports

from Home.models import Category

from adminside.models import Citymaster


def categoryproduct(request, cid):
    products_list = Product.objects.filter(avail="Available", category_id=cid)
    page = request.GET.get('page', 1)
    paginator = Paginator(products_list, 2)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, "listing.html", {"products": products, 'total': products_list.count()})


def viewallads(request):
    template = "listing.html"
    page = request.GET.get('page', 1)
    allads_list = Product.objects.filter(avail="Available")
    paginator = Paginator(allads_list, 2)
    try:
        allads = paginator.page(page)
    except PageNotAnInteger:
        allads = paginator.page(1)
    except EmptyPage:
        allads = paginator.page(paginator.num_pages)

    return render(request, template, {"ads": allads, 'total': allads_list.count()})


def addetails(request, pk):
    template = "detail.html"
    details = get_object_or_404(Product, pk=pk)
    details.adviewed += 1
    additionaldata = MachineReports.objects.get(Adid_id=details.id)
    details.save()
    return render(request, template, {'details': details, 'moredata': additionaldata})


def searchedad(request):
    category = request.GET.get('category', '')
    # print(category)

    # city = request.GET.get('cityfromlist', request.session['city'])
    if (request.GET.get('cityfromlist','')==""):
        city=request.session['city']
    else:
        city=request.GET.get('cityfromlist','')
    # print(city)
    sortby = request.GET.get('sortby', '')

    # print(sortby)
    if (request.GET.get('cityfromlist', '') == ""):
        authcity = request.user.profile.city_id
    else:
        authcity = request.GET.get('cityfromlist', '')

    if request.user.is_anonymous:
        if category == "":
            if sortby != "":
                searched_list = Product.objects.filter(title__icontains=request.GET['searchstring'], avail="Available",
                                                   Owner_name__profile__city_id=city).order_by(sortby)
            else:
                searched_list = Product.objects.filter(title__icontains=request.GET['searchstring'], avail="Available",
                                                   Owner_name__profile__city_id=city)
        else:
            if sortby != "":
                searched_list = Product.objects.filter(title__icontains=request.GET['searchstring'],category_id=category, avail="Available",
                                                       Owner_name__profile__city_id=city).order_by(sortby)
            else:
                searched_list = Product.objects.filter(title__icontains=request.GET['searchstring'], category_id=category,avail="Available",
                                                       Owner_name__profile__city_id=city)
        page = request.GET.get('page', 1)
        paginator = Paginator(searched_list, 2)
        try:
            searched = paginator.page(page)
        except PageNotAnInteger:
            searched = paginator.page(1)
        except EmptyPage:
            searched = paginator.page(paginator.num_pages)
        return render(request, "listing.html",
                      {'result': searched, 'string': request.GET['searchstring'],'sortby':sortby,'place':city,'category':category, 'total': searched_list.count(),
                       'categories': Category.objects.all(),
                       'locations': Citymaster.objects.filter(State_id=random.choice([1, 2]))})

    else:

        if category == "":
            if sortby != "":
                searched_list = Product.objects.filter(title__icontains=request.GET['searchstring'], avail="Available",
                                                   Owner_name__profile__city_id=authcity).order_by(sortby)
            else:
                searched_list = Product.objects.filter(title__icontains=request.GET['searchstring'], avail="Available",
                                                   Owner_name__profile__city_id=authcity)
        else:
            if sortby != "":
                searched_list = Product.objects.filter(title__icontains=request.GET['searchstring'],category_id=category, avail="Available",
                                                       Owner_name__profile__city_id=authcity).order_by(sortby)
            else:
                searched_list = Product.objects.filter(title__icontains=request.GET['searchstring'], category_id=category,avail="Available",
                                                       Owner_name__profile__city_id=authcity)

        # searched_list = Product.objects.filter(title__icontains=request.GET['searchstring'], avail="Available",
        #                                        category_id=request.GET['category'],)
        page = request.GET.get('page', 1)
        paginator = Paginator(searched_list, 2)
        try:
            searched = paginator.page(page)
        except PageNotAnInteger:
            searched = paginator.page(1)
        except EmptyPage:
            searched = paginator.page(paginator.num_pages)
        return render(request, "listing.html",
                      {'result': searched, 'string': request.GET['searchstring'], 'total': searched_list.count(),
                       'categories': Category.objects.all(),'sortby':sortby,'place':city,'category':category,
                       'locations': Citymaster.objects.filter(State_id=request.user.profile.state_id)})
