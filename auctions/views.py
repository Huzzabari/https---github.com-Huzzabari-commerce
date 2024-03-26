from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Auction, Bids, Comments, UserProfile
from .forms import AuctionForm, BidForm, WatchForm
import logging

def index(request):
    return render(request, "auctions/index.html", {'auctions': Auction.objects.all()})
    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            userprof=UserProfile.objects.create(user=user)
            userprof.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):            # post request takes the form data and makes a form from auction forms and if valid it stores all the information and saves it then returns to the index page.
    if request.method=="POST":
        form=AuctionForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category']
            category, created = Category.objects.get_or_create(name=category_name)
            auction=Auction(title=form.cleaned_data['title'],description=form.cleaned_data['description'],starting_bid=form.cleaned_data['starting_bid'],image_url=form.cleaned_data['image_url'], category=category )
            auction.save()
            return HttpResponseRedirect(reverse("index"))

    form=AuctionForm()              # otherwise it just goes to the create page and creates a form for the auction
    return render(request,"auctions/create.html", {"form":form})

def listing(request, pk):                        # If the listing has a post request it creates a bid form with a csrf token and checks if the form data is valid
    if request.method=="POST":
        form=BidForm(request.POST)               # request bid form object.
        auction=Auction.objects.get(pk=pk)         # get auction object class for the primary key
        if form.is_valid():
            new_bid=form.cleaned_data["new_bid"]                # if the form is valid the new bid field gets the bidform clean data of new bid
            if new_bid >= auction.starting_bid and new_bid > auction.highest_bid:       # if new bid is higher then save it to the auction form and go back to index.
                auction.highest_bid=new_bid
                auction.save()
                return HttpResponseRedirect(reverse("index"))
        
        user_profile= UserProfile.objects.get(user=request.user)  #get user profile instance
        watchlist=user_profile.watchlist.all()                # get everything from the users watchlist
        auction=Auction.objects.get(pk=pk)                        # get the instance of the auction the user is looking at
        if auction in watchlist:                              # if the auction is in the watchlist during a post request then remove it, otherwise add it.
            user_profile.watchlist.remove(auction)
            return HttpResponseRedirect(reverse("index"))
        user_profile.watchlist.add(auction)
        return HttpResponseRedirect(reverse("index"))
        
    #GET REQUEST    
    user=request.user                                                   # Otherwise it creates a bid form that has the auction id and user info hidden
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return render(request, "auctions/register.html")
    watchlist=user_profile.watchlist.all()
    auction=Auction.objects.get(pk=pk)                                   
    form = BidForm(initial={'auction_id': auction.id,"user":user.id})               
    return render(request, "auctions/listing.html", {'auction':auction,"form":form, 'watchlist': watchlist})

def watchlist(request):    #watchlist should be a post request to save the info, and a get request to view a users watchlist
    user_profile= UserProfile.objects.get(user=request.user)
    watchlist=user_profile.watchlist.all()
    return render (request, "auctions/watchlist.html", {'watchlist':watchlist})

def categories(request):  #categories page should be a post request and show all the listings of a specific category
    pass