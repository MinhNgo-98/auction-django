from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal


class User(AbstractUser):
    pass


class Listing(models.Model):
    CATEGORY = (
        ("Animals", "Animals"),
        ("Electronics", "Electronics"),
        ("Fashion", "Fashion"),
        ("Housing", "Housing"),
        ("Media", "Media"),
        ("Services", "Services"),
        ("Sports", "Sports")
    )
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=640)
    image_url = models.URLField(
        max_length=200, default="https://www.cowgirlcontractcleaning.com/wp-content/uploads/sites/360/2018/05/placeholder-img.jpg", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="owner")
    category = models.CharField(
        max_length=64, blank=True, null=True, choices=CATEGORY)
    watchlist = models.ManyToManyField(
        User, blank=True, related_name="watchlist")
    addedToWatchlist = models.BooleanField(default=False)
    winner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, related_name="winner")
    isClosed = models.BooleanField(default=False)


class Bid(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    bidValue = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    validBid = models.BooleanField(default=True)


class Comment(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=64)
