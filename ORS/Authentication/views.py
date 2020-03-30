from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.postgres import serializers
from django.core.serializers import json, serialize
from django.forms import model_to_dict
from django.http import JsonResponse
# Create your views here.
from Home.models import Profile
from django.shortcuts import render

from adminside.models import CountryMaster, Statemaster, Citymaster


def validate_username_login(request):
    user = request.POST.get('login', '')
    password = request.POST.get('password', '')
    is_taken = User.objects.filter(username__iexact=user).exists()
    if user != '' and password != '':
        if is_taken:
            user = authenticate(username=user, password=password)
            if user:
                data = {
                    'is_taken': True,
                    'user': True,
                    'content': True
                }
                return JsonResponse(data)
            else:
                data = {'is_taken': True, 'user': False, 'content': True, 'error_msg': 'plz enter valid password'}
                return JsonResponse(data)
        else:
            data = {'is_taken': False, 'user': False, 'content': True, 'error_msg': 'plz enter valid username'}
            return JsonResponse(data)
    else:
        data = {
            'content': False
        }
        return JsonResponse(data)


def validate_username_register(request):
    fname = request.POST.get('firstname', '')
    # print(fname+" fname")
    lname = request.POST.get('lastname', '')
    # print(lname+" lname")
    username = request.POST.get('username', '')
    # print(username+" username")
    email = request.POST.get('email', '')
    # print(email+" email")
    password1 = request.POST.get('password1', '')
    # print(password1+" p1")
    password2 = request.POST.get('password2', '')
    # print(password2)
    phone = request.POST.get('phone', '')
    # print(ph+" ph")
    address = request.POST.get('address', '')
    # print(adr+ " adr")
    pincode = request.POST.get('pincode', '')
    # print(pin+ " pim")
    country = request.POST.get('country', '')
    # print(coun+ " con")
    state = request.POST.get('state', '')
    # print(st +" st")
    city =request.POST.get('city', '')
    birthdate = request.POST.get('birthdate', '')
    is_taken1 = User.objects.filter(username__iexact=username).exists()
    is_taken2 = User.objects.filter(email__iexact=email).exists()
    if username != '' and email != '' and password1 != '' and password2 != '' and phone != '' and address != '' and pincode != ''  and country != '' and state != '' and city != '' and birthdate != '' and fname != '' and lname != '':
        if is_taken1 is False and is_taken2 is False:
            # Country = CountryMaster.objects.filter(id=country)
            # print(Country)
            # State = Statemaster.objects.filter(id=state)
            # print(State)
            # City = Citymaster.objects.filter(id=city)
            # print(City)
            user = User.objects.create_user(username, email, password1, fname, lname)
            print(user)
            newuser = Profile.objects.create(phone=phone, address=address, pincode=pincode, country_id=country, state_id=state,city_id=city, Birthdate=birthdate, user=user)
            newuser.save()
            data = {
                'is_taken': False,
                'username': False,
                'content': True
            }
            return JsonResponse(data)
        elif is_taken1 is True and is_taken2 is False:
            data = {'is_taken': True, 'username': False, 'content': True, "error_msg": "username already exist"}
            return JsonResponse(data)
        elif is_taken1 is False and is_taken2 is True:
            data = {'is_taken': True, 'email': False, 'content': True, "error_msg": "email already exist"}
            return JsonResponse(data)
        else:
            data = {'is_taken': True, 'username': False, 'email': False, 'content': True,
                    "error_msg": "username and email already exist"}
            return JsonResponse(data)
    else:
        data = {
            'content': False
        }
        return JsonResponse(data)


def validate_forget_password_email(request):
    email = request.POST.get('email', '')
    taken = User.objects.filter(email__iexact=email).exists()
    if taken is True:
        data = {'user': True, 'content': True}
        return JsonResponse(data)
    elif taken is False and email is not '':
        data = {'user': False, 'content': True, "error_msg": "User not exist"}
        return JsonResponse(data)
    else:
        data = {'content': False, "error_msg": "Enter Registered email first"}
        return JsonResponse(data)


def get_Country(request):
    # data =CountryMaster.objects.all()
    # data = serializers.serialize('json', list(data), fields=('id', 'CountryName'))
    # data = json.loads(serialize('json',data))
    # data=json.dumps([dict(item) for item in CountryMaster.objects.all().values('id', 'CountryName')])
    # print(CountryMaster.objects.all().values('id', 'CountryName'))

    return JsonResponse({"data":list(CountryMaster.objects.all().values('id', 'CountryName'))})

def get_State(request):
    # print(request.GET['conid'])
    return JsonResponse({"State":list(Statemaster.objects.filter(Country_id=request.GET['conid']).values('id', 'StateName'))})

def get_City(request):
    return JsonResponse({"City":list(Citymaster.objects.filter(State_id=request.GET['stateid']).values('id', 'CityName'))})
