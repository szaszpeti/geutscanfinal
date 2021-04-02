from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import *
from pyuploadcare.dj.forms import ImageField

class PostForm(forms.ModelForm):
    photo = ImageField(label='')

    class Meta:
        model = Post
        fields = ('photo',)


class TechnicianForm(ModelForm):
	class Meta:
		model = Technician
		fields = '__all__'
		exclude = ['user']

class InspectionForm(ModelForm):
    photo = ImageField(label='')

    class Meta:
        model = Inspection
        fields = '__all__'

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
