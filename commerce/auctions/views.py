from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Watchlist, Bid, Comment

LISTING_CATEGORIES = [
    "General",
    "Outdoors",
    "Vehicle",
    "Education",
    "Music",
    "Games",
    "food"
]

def index(request):

    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


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

def create_listing(request):
    
    if request.method == "POST":
        name = request.POST["item_name"]
        description = request.POST["description"]
        price = request.POST["price"]
        category = request.POST["category"]
        image = request.POST["image"]
        listing = Listing(lister=request.user, item_name=name, description=description, price=price, category=category, image=image)
        listing.save()

    return render(request, "auctions/create_listing.html", {
        "categories": LISTING_CATEGORIES
    })

def listing(request, listing_id):

    listing = Listing.objects.get(pk=listing_id)

    try:
        watchlist = Watchlist.objects.get(watcher=request.user, listing=listing)
        watchlist = True
    except Watchlist.DoesNotExist:
        watchlist = False
    except TypeError:
        watchlist = False

    if request.method == "POST":

        if "watchlist_item" in request.POST:
            value = request.POST["watchlist_item"]
       
            if value == "add":
                new_watchlist = Watchlist(watcher=request.user, listing=listing)
                new_watchlist.save()
            else:
                Watchlist.objects.get(watcher=request.user, listing=listing).delete()

            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        
        if "bid" in request.POST:
            new_bid = float(request.POST["bid"])
            current_bid = listing.price

            if new_bid > current_bid:
                listing.price = new_bid
                listing.save()
                bid = Bid(bidder=request.user, listing=listing, bid=new_bid)
                bid.save()
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            else:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "bids": listing.listing_bids.all(),
                    "comments": listing.listing_comments.all(),
                    "in_watchlist": watchlist,
                    "bid_error": True
                })
        
        if "comment" in request.POST:
            new_comment = request.POST["comment"].strip()
            comment = Comment(commenter=request.user, listing=listing, content=new_comment)
            comment.save()
            
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "bids": listing.listing_bids.all(),
        "comments": listing.listing_comments.all(),
        "in_watchlist": watchlist
    })

def watchlist(request):
    
    watchlist = Watchlist.objects.filter(watcher=request.user)

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

def categories(request):
    
    return render(request, "auctions/categories.html", {
        "categories": LISTING_CATEGORIES
    })

def category(request, category):
    
    listings = Listing.objects.filter(category=category)

    return render(request, "auctions/category.html", {
        "listings": listings,
        "category": category
    })
