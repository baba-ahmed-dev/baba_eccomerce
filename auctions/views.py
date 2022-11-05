from django.contrib.auth import authenticate, login, logout
from django.core.checks import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, request
from django.http.response import HttpResponseBase
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib import messages

from .models import User ,Category ,Listing , Bid , Comment , Watchlist
from .forms import Categories, CreateList , NewBid , CreateComment

"""Index function return all active listings"""

listing = Listing.objects.filter(active=True)
def index(request):
    """Index function return all active listings"""
    return render(request, "auctions/index.html",{"listing":listing})

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

def categories(request ):
    """categories function return all categories exists"""
    catgs = Category.objects.all()
    create_cat = Categories()
    return render(request,"auctions/categories.html",{
        "catgs":catgs,
        "crca":create_cat
    })
def get_category(request, category):
    """function return all active listings in one category"""
    cat = Category.objects.get(id=category)
    categories = Listing.objects.filter(category=cat,active=True)
    return render(request,"auctions/categories.html",{
        "categories":categories,
        "cat":cat
    })
def create_category(request):
    if request.method == "POST":
        form = Categories(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("categories"))
        return HttpResponseRedirect(reverse("categories"))
    return HttpResponseRedirect(reverse("index"))

def create_listing(request):
    """function allow to the user to create listing and save it"""
    if request.method == "POST":
        form = CreateList(request.POST,request.FILES)
        if form.is_valid():
            category = form.cleaned_data["category"]
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            startbid = form.cleaned_data["startbid"]
            image = form.cleaned_data["image"]
            user = request.user
            post = Listing(category=category, name=name, description=description, startbid=startbid, image=image,user=user)
            post.save()
            return HttpResponseRedirect(reverse("index"))
    return render(request,"auctions/listing.html",{
        "new_listing":CreateList()
    })

def details(request, id):
    """details function return one listing with all informations"""
    if id:
        list = Listing.objects.get(id=id) 
        bid_form = NewBid()
        comment_form = CreateComment()
        return render(request,"auctions/details.html",{
            "listing":list,
            "bid":bid_form,
            "comment_form":comment_form,
            "comments":Comment.objects.filter(list=list),
        })
    return render(request,"auctions/index.html",{})


def watchlist(request):
    """function return to the user all active listings exsist in her watchlist page"""
    ids = User.objects.get(id=request.user.id).watchlist.values_list("userlist")
    watchlist_items = Listing.objects.filter(id__in=ids)
    return render(request,"auctions/watchlist.html",{
        "watchlist":watchlist_items
        })

def watch(request,id):
    """watch function allow to the user to add a listing to her watchlist page"""
    ids = User.objects.get(id=request.user.id).watchlist.values_list("userlist")
    watchlist_items = Listing.objects.filter(id__in=ids)
    list = Listing.objects.get(id=id)
    if list in watchlist_items:
        item = Watchlist.objects.filter(username=request.user,userlist=list)
        item.delete()
        return HttpResponseRedirect(reverse("watchlist"))
    else:
        adding = Watchlist(username=request.user)
        adding.save()
        adding.userlist.add(list) 
        adding.save()
        return HttpResponseRedirect(reverse("watchlist"))

def process_comment(request, id):
    """function retrieve comment_information from comment_form and save it"""
    if request.method == "POST":
        comnt = CreateComment(request.POST)
        list = Listing.objects.get(id=id)
        if comnt.is_valid():
            text = comnt.cleaned_data["text"]
            us = request.user
            new_comment = Comment(text=text,list=list ,user=us)
            new_comment.save()
            return HttpResponseRedirect(reverse("details", args=[id]))
        return HttpResponseRedirect(reverse("details", args=[id]))
    return render(request, "auctions/index.html")
            
def process_bid(request, id):
    """function retrieve bid_information from bid_form and save it than update current price"""
    if request.method == "POST":
        list = Listing.objects.get(id=id)
        new_bid = NewBid(request.POST)
        if new_bid.is_valid():
            us = request.user
            current_Price = new_bid.cleaned_data["amount"]
            price = list.startbid
            if current_Price > price :
                bid = Bid(amount=current_Price,user=us,list=list)
                bid.save()
                Listing.objects.filter(name=list).update(startbid=current_Price)
                return HttpResponseRedirect(reverse("details", args=[id]))
            else:
                return HttpResponseRedirect(reverse("details",args=[id]))           
    return HttpResponseRedirect(reverse("index"))

def close(request, id):
    """function close the listing and specify the winner"""
    list = Listing.objects.get(id=id)
    list_has_bid=Bid.objects.filter(list=list)
    if list_has_bid:
        lb = list.startbid
        bd = Bid.objects.get(amount=lb, list=list)
        winner = bd.user
        name = list.name
        Listing.objects.filter(id=id).update(active=False)
        return render(request,"auctions/index.html",{
          "listing":listing,
         "message":f"Bid {name} won by {winner}"
        })
    else:
        Listing.objects.filter(id=id).update(active=False)
        return render(request,"auctions/index.html",{
          "listing":listing,
        })
