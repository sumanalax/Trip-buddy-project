from django.shortcuts import render, redirect
from .models import User, TravelTrip
from django.contrib import messages
from datetime import date    
from django.utils.dateparse import parse_date

def index(request):
    return render(request,'TripBuddy_app/index.html')
    

def register(request):
    results = User.objects.register(request.POST)
    if results[0]:
        request.session["user_id"] = results[1].id
        return redirect("/travel")
    else:
        for error in results[1]:
            messages.add_message(request, messages.ERROR, error)
        return redirect ("/")

def login(request):
    results = User.objects.login(request.POST)
    if results[0]:
        for i in results[1]:
            request.session["user_id"] = i.id
            request.session["first_name"] = i.first_name
            break
        return redirect("/travel")
    else:
        for error in results[1]:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/")

def travel(request):
    if "user_id" not in request.session:
        messages.add_message(request, messages.ERROR,"You need to  login first")
        return redirect("/")
    if "user_id" in request.session:
        for key, value in request.session.items():
            if key == 'user_id':
                my_trips = TravelTrip.objects.filter(user_id=value)
                other_trips = TravelTrip.objects.filter().exclude(user_id=value).exclude(user_id=0)
    trips_info={
        'other_trips': other_trips,
        'my_trips': my_trips
        }
    return render(request, "TripBuddy_app/travel.html", trips_info)

def addtrip(request):
    return render(request,'TripBuddy_app/add_trip.html')

def savetrip(request):
    results = TravelTrip.objects.savetrip(request.POST)
    return redirect('/travel')

def canceltrip(request):
    trip_id = request.path[len('/canceltrip/'):]
    if "user_id" in request.session:
        for key, value in request.session.items():
            if key == 'user_id':
                canceltrip = TravelTrip.objects.filter(id=trip_id).filter(user_id=value).update(user_id=0)
    return redirect('/travel')

def jointrip(request):
    trip_id = request.path[len('/jointrip/'):]
    if "user_id" in request.session:
        for key, value in request.session.items():
            if key == 'user_id':
                errors = []
                trip_info = TravelTrip.objects.get(id=trip_id)
                trip_group = TravelTrip.objects.filter(destination=trip_info.destination).filter(user_id=value)
                if(len(trip_group) == 0):
                    traveltrip = TravelTrip.objects.create(
                            destination = trip_info.destination,
                            description = trip_info.description,
                            travel_date_from = trip_info.travel_date_from,
                            travel_date_to = trip_info.travel_date_to,
                            user_id = User.objects.get(id=value)
                            )
                else:
                    errors.append("Already added to the trip")
    return redirect('/travel')


def deletetrip(request):
    trip_id = request.path[len('/deletetrip/'):]
    deletetrip = TravelTrip.objects.filter(id=trip_id).delete()
    return redirect('/travel')

def viewtrip(request):
    trip_group={}
    trip_id = request.path[len('/viewtrip/'):]
    trip_info = TravelTrip.objects.filter(id=trip_id)
    users_info = User.objects.all()
    if "user_id" in request.session:
        for key, value in request.session.items():
            if key == 'user_id':
                for i in trip_info:
                    trip_group_users = TravelTrip.objects.filter(destination=i.destination).exclude(user_id=value).exclude(id=0)

    trip_context={
        'trip': trip_info,
        'users': users_info,
        'group': trip_group_users
    }
    return render(request,'TripBuddy_app/view_trip.html', trip_context)
