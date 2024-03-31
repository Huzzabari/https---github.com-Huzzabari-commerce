from django.contrib.auth import authenticate, login, logout
from django.db.models import Max
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Auction, Bids, Comments, UserProfile
from .forms import AuctionForm, BidForm, CommentForm
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
            auction=Auction(title=form.cleaned_data['title'],description=form.cleaned_data['description'],starting_bid=form.cleaned_data['starting_bid'],image_url=form.cleaned_data['image_url'], category=category, creator=request.user )
            auction.save()
            return HttpResponseRedirect(reverse("index"))

    form=AuctionForm()              # otherwise it just goes to the create page and creates a form for the auction
    return render(request,"auctions/create.html", {"form":form})


def listing(request, pk):
    if request.method == "GET":
        user=request.user                                                   # Otherwise it creates a bid form that has the auction id and user info hidden
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=request.user)
        else:
            messages.warning(request, 'Please Register an account')
            return render(request, "auctions/register.html")
        watchlist=user_profile.watchlist.all()              # get watchlist of user and the auction object and comment object
        auction=Auction.objects.get(pk=pk)    
        comments=Comments.objects.filter(auction_id=pk)                               
        form1 = BidForm(initial={'auction_id': auction.id,"user":user.id})     # create a bid and comment form
        form2=CommentForm(initial={'auction_id': auction.id,"user":user.id})             
        return render(request, "auctions/listing.html", {'auction':auction,"form1":form1, "form2":form2, 'watchlist': watchlist, "comments":comments, "creator": auction.creator, "user":user, "is_open": auction.is_open, "winner":auction.winner}) 
                # Include auction, form1, form2, watchlist, comments, creator of the auciton, and user
    elif request.method=="POST":
        if 'form1' in request.POST:
            form1 = BidForm(request.POST)
            auction = Auction.objects.get(pk=pk)                    # gets a bidform post requestion and saves the info in form 1
            if form1.is_valid():
                new_bid = form1.cleaned_data["new_bid"]              # if the form is valid clean the new_bid data and if the bid is higher than the starting and highest bid, then it becomes the highest bid.
                if new_bid >= auction.starting_bid and new_bid > auction.highest_bid:
                    auction.highest_bid = new_bid
                    auction.winner= request.user                               # make the auction winner the current user who did this bid.
                    auction.save()
                    bid = Bids(auction=auction, bids=new_bid, user=request.user)           # save this bid by importing the Bids model and creating an instance.  save the auction, new bid, and user
                    bid.save()
                    return HttpResponseRedirect(reverse("listing", args=[pk]))
                else:
                    messages.warning(request, 'BID NOT HIGH ENOUGH') 
                    return HttpResponseRedirect(reverse("listing", args=[pk]))
            else:
                print("Form is not valid")
                
        elif 'form2'in request.POST:                                 # made a change to have 2 forms.  form two post does something different.
            form2=CommentForm(request.POST)
            if form2.is_valid():                                         # form for submitting comments
                new_comment=form2.cleaned_data["comments"]
                user_id = UserProfile.objects.get(user=request.user).id
                comments=Comments.objects.create(auction_id=pk, user_id=user_id, comments=new_comment)
                return HttpResponseRedirect(reverse("listing", args=[pk]))
            
        elif 'watchlist' in request.POST:   
            user_profile= UserProfile.objects.get(user=request.user)  #get user profile instance
            user_id = user_profile.id  # get user profile id
            watchlist=user_profile.watchlist.all()                # get everything from the users watchlist
            auction=Auction.objects.get(pk=pk)                        # get the instance of the auction the user is looking at
            if auction in watchlist:                              # if the auction is in the watchlist during a post request then remove it, otherwise add it.
                user_profile.watchlist.remove(auction)
                return HttpResponseRedirect(reverse('watchlist'))
            user_profile.watchlist.add(auction)
            return HttpResponseRedirect(reverse('watchlist'))
        
        elif 'close' in request.POST:                           # If the post request is close, then we plan to close the auction and name a user the winner.
            auction=Auction.objects.get(pk=pk)
            auction.is_open=False                                       # so the auction is no longer open
            bids=Bids.objects.filter(auction=auction)                   # make an instance of bid fromt he bid object that is tied to the auction the user is viewing
            max_bid_dict=bids.aggregate(Max('bids'))                    # find the maximum bid of the auction
            max = max_bid_dict['bids__max']                              # max bid was in a dictionary.  so now it's just the max bid
            if max is not None:
                bid_obj = Bids.objects.get(bids=max)                       # If the max bid isn't none, then get the bid object tied to that max
                auction.winner = bid_obj.user                               # make the winner of the auction the user of that bid object and save the auction
                auction.save()
                return HttpResponseRedirect(reverse("index"))
            else:               
                messages.warning(request, 'NO ONE HAS BID YET')
                auction.is_open=True 
                return HttpResponseRedirect(reverse("listing", args=[pk]))
    return HttpResponse("Something went wrong")        
  

def watchlist(request):    #watchlist should be a post request to save the info, and a get request to view a users watchlist
    user_profile= UserProfile.objects.get(user=request.user)
    watchlist=user_profile.watchlist.all()
    return render (request, "auctions/watchlist.html", {'watchlist':watchlist})

def categories(request):  #categories page should be a post request and show all the listings of a specific category
    category=Category.objects.all()
    return render(request, "auctions/categories.html", {'categories': category})

def category(request, category_name):
    category=Category.objects.get(name=category_name)
    auctions=Auction.objects.filter(category=category)
    return render(request, "auctions/category.html", {'category': category, 'auctions': auctions})
 