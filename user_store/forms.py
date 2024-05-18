from django.contrib.auth.forms import UserCreationForm,UserChangeForm,AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Products,Comments


# User signup form
class UserSignupForm(UserCreationForm):
  password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
  password2 = forms.CharField(label='Password Conform',widget=forms.PasswordInput(attrs={'class':'form-control'}))
  class Meta:
    model = User
    fields = ['nuserame','email']
    widgets = {
      'username':forms.TextInput(attrs ={ 'class':'form-control'}),
      'email':forms.EmailInput(attrs ={ 'class':'form-control'}),
    }


class LoginForm(AuthenticationForm):
  username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


class WebsiteLoginForm(AuthenticationForm):
  # def _init_(self,args,*kwargs):
  #   super()._init_(args,*kwargs)
  #   self.fields.pop('username')
  username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Your Username'}))
  password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))



class User_product_data(forms.ModelForm):
    class Meta:
      model = Products
      fields = ['title','description','image','price']
      widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control bg-secondary-light', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control bg-secondary-light', 'placeholder': 'Description'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'price': forms.NumberInput(attrs={'class': 'form-control bg-secondary-light', 'placeholder': 'Price'}),
        }

class User_comment(forms.ModelForm):
  class Meta:
    model = Comments
    fields = ['comment']