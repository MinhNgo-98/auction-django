from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime
from django import forms
from .models import User, Listing, Bid, Comment


class AddListingForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(), label="Title")
    description = forms.CharField(widget=forms.Textarea(), label="Description")
    image_url = forms.CharField(widget=forms.TextInput(), label="Image")
    price = forms.DecimalField(widget=forms.TextInput(), label="Starting Bid")
    category = forms.ChoiceField(choices=Listing.CATEGORY, label="Category")


class SubmitBidForm(forms.Form):
    bid = forms.DecimalField(widget=forms.TextInput(), label="Bid")


class AddCommentForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(), label="Title")
    description = forms.CharField(
        widget=forms.Textarea(), label="Your comment")


def index(request):
    listings = Listing.objects.filter(isClosed=False)
    title = "Active listings"
    return render(request, "auctions/index.html", {"listings": listings, "title": title})


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


@login_required
def add_listing(request):
    # if form submitted, store data into the model
    if request.method == 'POST':
        form = AddListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            image_url = form.cleaned_data["image_url"]
            price = form.cleaned_data["price"]
            category = form.cleaned_data["category"]
            owner = request.user
            listing_instance = Listing.objects.create(
                title=title, price=price, description=description, image_url=image_url, category=category, owner=owner)
            return render(request, "auctions/add_listing.html", {"addListingForm": AddListingForm()})

        else:
            """error page"""
    # if add page called, render add page
    else:
        return render(request, "auctions/add_listing.html", {"addListingForm": AddListingForm()})


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = Comment.objects.filter(listing=listing)
    bid = Bid(user=request.user, listing=listing)
    owner = str(listing.owner)
    winner = str(listing.winner)
    return render(request, "auctions/listing.html", {"listing": listing, "bid": bid, "comments": comments, "submitBidForm": SubmitBidForm(), "addCommentForm": AddCommentForm, "owner": owner, "winner": winner})


def all_listings(request):
    listings = Listing.objects.all()
    title = "All listings"
    return render(request, "auctions/index.html", {"listings": listings, "title": title})


@login_required
def add_to_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    request.user.watchlist.add(listing)
    listing.addedToWatchlist = True
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required
def remove_from_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    request.user.watchlist.remove(listing)
    listing.addedToWatchlist = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required
def watchlist(request):
    watchlist = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {"watchlist": watchlist})


@login_required
def submit_bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = Comment.objects.filter(listing=listing)
    bid = Bid(user=request.user, listing=listing)
    owner = str(listing.owner)
    winner = str(listing.winner)
    if request.method == 'POST':
        form = SubmitBidForm(request.POST)
        if form.is_valid():
            bidValue = form.cleaned_data["bid"]
            if bidValue > listing.price:
                bid.bidValue = bidValue
                bid.validBid = True
                bid.save()
                listing.price = bidValue
                listing.save()
            elif bidValue <= listing.price:
                bid.validBid = False
                bid.save()
            if request.user.is_authenticated:
                username = request.user.username
    return render(request, "auctions/listing.html", {"listing": listing, "bid": bid, "comments": comments, "submitBidForm": SubmitBidForm(), "addCommentForm": AddCommentForm, "owner": owner, "winner": winner, "currentUser": username})


@login_required
def close_bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bid = Bid.objects.filter(listing=listing).latest('listing')
    listing.isClosed = True
    listing.winner = bid.user
    listing.save()
    return HttpResponseRedirect(reverse("index"))


@login_required
def add_comment(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(pk=listing_id)
        comment = Comment(listing=listing, user=request.user)
        form = AddCommentForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            comment.title = title
            comment.description = description
            comment.save()
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def categories(request):
    categories = set(
        [category[0] for category in Listing.CATEGORY])
    return render(request, "auctions/categories.html", {"categories": sorted(categories)})


def category(request, category):
    listings = Listing.objects.filter(category=category, isClosed=False)
    title = category
    return render(request, "auctions/index.html", {"listings": listings, "title": title})
