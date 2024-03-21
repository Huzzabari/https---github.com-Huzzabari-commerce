from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Auction, Bids, Comments, UserProfile
from .forms import AuctionForm, BidForm


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


def create(request):
    if request.method=="POST":
        form=AuctionForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category']
            category, created = Category.objects.get_or_create(name=category_name)
            auction=Auction(title=form.cleaned_data['title'],description=form.cleaned_data['description'],starting_bid=form.cleaned_data['starting_bid'],image_url=form.cleaned_data['image_url'], category=category )
            auction.save()
            return HttpResponseRedirect(reverse("index"))

    form=AuctionForm()
    return render(request,"auctions/create.html", {"form":form})

def listing(request, pk):
    if request.method=="POST":
        form=BidForm(request.POST)
        if form.is_valid():
            auction=Auction.objects.get(pk=pk)
            bid=Bids(auction=form.cleaned_data["auction"], bids=form.cleaned_data["bids"], user=form.cleaned_data["user"])
            if bid.bids > auction.starting_bid:
                auction.starting_bid=bid.bids
                auction.save()
                bid.save()
                return HttpResponseRedirect(reverse("index"))
    user=request.user        
    auction=Auction.objects.get(pk=pk)
    form = BidForm(initial={'auction_id': auction,"user":user})
    return render(request, "auctions/listing.html", {'auction':auction,"form":form})

def watchlist(request):
    pass

def categories(request):
    pass