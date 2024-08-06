from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Additional_Fiels

class RegisterForm(UserCreationForm):
    first_name=forms.CharField(max_length=50, widget=forms.TextInput (attrs ={'class':'form-control'}))
    last_name=forms.CharField(max_length=50, widget=forms.TextInput (attrs ={'class':'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput (attrs ={'class':'form-control'} ))

    class Meta:
        model=User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class']='form-control' 
        self.fields['password1'].widget.attrs['class']='form-control' 
        self.fields['password2'].widget.attrs['class']='form-control' 

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model= Additional_Fiels
        fields= ["phone_number", "rollno"]
        