from django import forms
from django.forms import ModelForm , TextInput
from .models import Category, Listing , Bid, Comment


class Categories(ModelForm):
    name = forms.CharField(max_length=14,label="", widget=forms.TextInput(attrs={"placeholder":"Add category : "}))
    class Meta:
        model = Category
        fields = ["name"]

class CreateList(ModelForm):
    class Meta:
        model = Listing
        fields = ["category","name","description","startbid","image"]

class NewBid(ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]

class CreateComment(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]