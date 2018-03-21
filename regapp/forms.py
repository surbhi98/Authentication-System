from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile



class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class UserLoginForm(forms.Form):
    username=forms.CharField()
    #password=forms.CharField(widget=forms.PasswordInput)

    def clean(self,*args,**kwargs):
        username=self.cleaned_data.get("username")
        #password=self.cleaned_data.get("password")
        if username:
            #user=authenticate(username=username)
            user = User.objects.get(username=username)
            print(".........exist...........")
            if not user:
                print("....doesn't exist.............")
                raise forms.ValidationError("This user does'nt exist")
            #if not user.check_password(password):
             #   raise forms.ValidationError("Incorrect Password")
            if not user.is_active:
                print("............not active............")
                raise forms.ValidationError("This is not an active user")
        return super(UserLoginForm, self).clean(*args, **kwargs)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date')


        

class EditProfileForm(UserChangeForm):
    class Meta:
        model=User
        fields= ('username', 'first_name', 'last_name', 'email','password')

