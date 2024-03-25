from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Auction, Bids, Comments, UserProfile
from .forms import AuctionForm, BidForm
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
        form=BidForm(request.POST)
        print("Form data:", request.POST)
        print("Form errors:", form.errors)
        if form.is_valid():
            print("Form errors:", form.errors)
            print("Form is valid")   #  NOT GETTING THIS
            auction = Auction.objects.get(pk=form.cleaned_data["auction_id"])
            user = User.objects.get(pk=form.cleaned_data["user"])
            bids = Bids(auction=auction, bids=form.cleaned_data["new_bid"], user=user)
            print("Auction ID:", form.cleaned_data["auction_id"])
            print("New Bid:", form.cleaned_data["new_bid"])
            print("User:", form.cleaned_data["user"])
            #logging.info(bids)
            #logging.info(auction)
            if bids.bids >= auction.starting_bid and bids.bids > auction.highest_bid:
                auction.highest_bid=bids.bids
                auction.save()
                bids.save()
                return HttpResponseRedirect(reverse("index"))
        #return HttpResponseRedirect(reverse("index"))
    user=request.user                                                   # Otherwise it creates a bid form that has the auction id and user info hidden
    auction=Auction.objects.get(pk=pk)
    form = BidForm(initial={'auction_id': auction,"user":user})               
    return render(request, "auctions/listing.html", {'auction':auction,"form":form})

def watchlist(request):    #watchlist should be a post request to save the info, and a get request to view a users watchlist
    pass

def categories(request):  #categories page should be a post request and show all the listings of a specific category
    pass