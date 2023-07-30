from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control, never_cache
from django.contrib import messages

# Create your views here.

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def HomePage(request):
    
    return render(request,'home.html')

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @never_cache
def SignUpPage(request):
    if 'username' in request.session:
        return redirect('home')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        
        if not (username and email and pass1 and pass2):
                messages.info(request,"Please fill required field")
                return redirect('signup')
        
        elif pass1 != pass2:
                messages.info(request,"Password mismatch")
                return redirect('signup')
        else:
             if User.objects.filter(username = username).exists():
                messages.info(request,"Username Already Taken")
                return redirect('signup')
                
             elif User.objects.filter(email = email).exists():
                 messages.info(request,"Email Already Taken")
                 return redirect('signup')
             else:
                my_user = User.objects.create_user(username,email,pass1)
                my_user.save()
                
        return redirect('login')
        
    
    return render(request,'signup.html')

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def LoginPage(request):
    if 'username' in request.session:
        return redirect('home')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request,username=username,password = pass1)
        if user is not None:
            request.session['username'] = username
            login(request,user)
            return redirect('home')
        else:
            return HttpResponse("Username or Password is Incorrect!!!")
    return render(request,'login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def LogOutPage(request):
    if 'username' in request.session:
        del request.session['username']
        logout(request)
        return redirect('login')