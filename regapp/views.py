from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import SignUpForm, UserLoginForm, ProfileForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_text
#from myapp.models import Product
#from .models import Items
from django.db.models import Sum
import jwt



    
def our(request):
    return render(request,'base.html')
    

def signup(request):
    #form=SignUpForm()
    if request.method == 'POST':
        print("..form...............")
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            print("..........valid......")
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': jwt.encode({'id': user.id, 'email': user.email}, "SECRET_KEY")
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
        else:
            form = SignUpForm()
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@transaction.atomic
def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')

def activate(request, uidb64, token):
    uid = force_text(urlsafe_base64_decode(uidb64))
    #user = User.objects.get(pk=uid)
    #print(user)
    payload = jwt.decode(token, "SECRET_KEY")
    print(payload)
    email = payload['email']
    userid = payload['id']
    print(email)
    user = User.objects.get(pk= userid, email = email)
    if user:
        print(".......................................")
        #u = user.objects.get(email = email, id= userid)
        login(request, user)
        return redirect('view_profile')
    else:
        return HttpResponse("invalid user credentials")
                            
def login_view(request):
    title="login"
    form= UserLoginForm(request.POST or None)
    print("................errror..................")
    if form.is_valid():
        username=form.cleaned_data.get('username')
        #password=form.cleaned_data.get('password')
        user= User.objects.get(username=username)
        #user= authenticate(username=username)
        current_site = get_current_site(request)
        if user:
            payload = {'id': user.id,
                       'email': user.email,
                       }
            token = jwt.encode(payload, "SECRET_KEY")
        subject = 'Activate Your MySite Account'
        message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                #'token': account_activation_token.make_token(user),
                'token': jwt.encode({'id': user.id, 'email': user.email}, "SECRET_KEY")
            })
        user.email_user(subject, message)
        return redirect('account_activation_sent')
        #login(request,user)
        #print(request.user.is_authenticated())
        #return redirect('our')
    return render(request, 'login.html', {'form': form})

def view_profile(request):
    #user_form = UserCreationForm(instance=request.user)
    #profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'user':request.user, 'profilee': request.user.profile})

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            #messages.success(request, _('Your profile was successfully updated!'))
            return redirect('view_profile')
        else:
            return render(request, 'edit_profile.html', {'user_form': user_form})
         #   messages.error(request, _('Please correct the error below.'))
    else:
        user_form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def change_password(request):
    if request.method == 'POST':
        user_form = PasswordChangeForm(data=request.POST, user=request.user)
        if user_form.is_valid():
            user_form.save()
            update_session_auth_hash(request, user_form.user)
            #messages.success(request, 'Your password was updated successfully!')  
            #changed = 'Password updated successfully'
            return redirect('view_profile')
        else:
            #m=messages.error(request, 'Document deleted.')
            #messages.error(request, _('Old password did not match'))
            return render(request,'changePassword.html', {'user_form': user_form })
            #messages.error(request, _('Old password does not match'))
    else:
        user_form = PasswordChangeForm(user=request.user)
    return render(request, 'changePassword.html', {
        'user_form': user_form,
        
    })


def logout_view(request):
    logout(request)
    print(request.user.is_authenticated())
    return redirect('our')

