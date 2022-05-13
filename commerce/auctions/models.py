from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ImageField
from flask import render_template


class User(AbstractUser):
    pass

class Listing(models.Model):
    lister = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    item_name = models.CharField(max_length=500, default="")
    description = models.CharField(max_length=500, default="")
    category = models.CharField(max_length=64, default="")
    price = models.FloatField()
    image = models.URLField(max_length=200, default="https://i.guim.co.uk/img/media/26392d05302e02f7bf4eb143bb84c8097d09144b/446_167_3683_2210/master/3683.jpg?width=1200&height=1200&quality=85&auto=format&fit=crop&s=49ed3252c0b2ffb49cf8b508892e452d")

    def __str__(self):
        return f"{self.item_name}"

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    content = models.CharField(max_length=500, default="")

    def __str__(self):
        return f"{self.content}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    bid = models.FloatField()

    def __str__(self):
        return f"{self.bid}"

class Watchlist(models.Model):
    watcher = models.ForeignKey(User, on_delete=models.CASCADE,related_name="watchlists")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.watcher}, {self.listing}"
