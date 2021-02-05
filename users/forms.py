# users/forms.py
from django.contrib.auth.forms import UserCreationForm
from django import forms
from users import models

# create a custom user with email field.
class CustomUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		fields = UserCreationForm.Meta.fields + ("email",)

# create a discussion post.
class CreatePostForm(forms.Form):
	title = forms.CharField(max_length=60, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Post Title"}), required=True)
	body = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter post details"}), required=True)
	author = forms.CharField(max_length=60, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"}), required=True)
	category = forms.ChoiceField(choices=models.CAT_CHOICES, widget=forms.Select(), required=True)

# create a comment.
class CommentForm(forms.Form):
	author = forms.CharField(max_length=60, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name"}), required=True)
	body = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Leave a comment!"}), required=True)