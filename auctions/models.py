from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

from django.db.models.base import Model


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=14)

    def __str__(self):
        return self.name


class Listing(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=14)
    description = models.TextField()
    startbid = models.DecimalField(max_digits=7 , decimal_places=2)
    created = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="images%y%m%d", default="https://www.google.com/url?sa=i&url=http%3A%2F%2Fzifundise.com%2Fblogs-and-letters%2F&psig=AOvVaw1Y_-_eMrbMzbtrV8o4h-aq&ust=1641069582490000&source=images&cd=vfe&ved=0CAsQjRxqFwoTCMjztYKxjPUCFQAAAAAdAAAAABAD")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userlisting")
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.name

class Bid(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name="bids")
    list = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    class Meta:
        ordering = ["-amount"]

    def __str__(self):
        return f"Bid {self.id}: {self.amount} on {self.list.name} by {self.user.username}"

class Comment(models.Model):
    text = models.TextField()
    created = models.DateTimeField(auto_now=True)
    list = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"Comment on {self.list.name} by {self.user.username}"

class Watchlist(models.Model):
    username = models.ForeignKey(User , on_delete=models.CASCADE,related_name="watchlist")
    userlist = models.ManyToManyField(Listing, blank=True)

    def __str__(self):
        return f"watchlist for {self.username}"
