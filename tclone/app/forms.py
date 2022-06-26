from django import forms
from django.forms import Textarea
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProfileEditForm(forms.ModelForm):

	name = forms.CharField(label='Name')
	bio = forms.CharField(label='Bio')
	class Meta:
		model = Profile
		fields = ['name','bio','profile_img']
		initial=123

class PostForm(forms.ModelForm): 
	text = forms.CharField(label='')
	text.widget.attrs.update({'class': 'text'})


	class Meta:
		model = Post
		fields ="__all__"
		exclude = ['author', 'likers', 'sharers','date']
		auto_id = False

class CommentForm(forms.ModelForm): 
	text = forms.CharField(label='')
	text.widget.attrs.update({'class': 'text'})


	class Meta:
		model = Comment
		fields ="__all__"
		exclude = ['author','date','post']
		auto_id = False
class NewUserForm(UserCreationForm):
	

	class Meta:
		model = User
		fields = ("username", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		
		if commit:
			user.save()
		return user