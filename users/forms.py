# users/forms.py

from django.contrib.auth.forms import UserCreationForm
from django import forms
from users import models

class CustomUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		fields = UserCreationForm.Meta.fields + ("email",)

class CreatePostForm(forms.Form):
	title = forms.CharField(max_length=60, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Post Title"}), required=True)
	body = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter post details"}), required=True)
	author = forms.CharField(max_length=60, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"}), required=True)
	category = forms.ChoiceField(choices=models.CAT_CHOICES, widget=forms.Select(), required=True)
	# category = forms.CharField(max_length=20, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Post Title"}), required=True)

class CommentForm(forms.Form):
	author = forms.CharField(max_length=60, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"}), required=True)
	body = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Leave a comment!"}), required=True)