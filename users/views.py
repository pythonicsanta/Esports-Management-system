from django.shortcuts import render,redirect
from . forms import UserRegisterForm,OrganizerRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from . models import User
# Create your views here.

def login_user(request):
    logout(request)
    username=password=''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user=authenticate(username = username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                messages.success(request,f'You are login!')
                return redirect('blog-home')
        else:
            messages.warning(request,f'Please enter a correct username and password. Note that both fields may be case-sensitive.')
            return redirect('login2')

    else:
        return render(request, 'users/log.html')



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Your Account has been created! You can now login!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html',{'form':form})

def organizer_register(request):
    if request.method == 'POST':
        form = OrganizerRegisterForm(data=request.POST)
        if form.is_valid():
            check=form.cleaned_data.get('account')
            #print("ye raha choice data",check)
            if check=='1':  #check must be true ..ie index 1 organizer
                user=form.save()
                #user.set_password(user.password)
                user.is_organizer = True
                user.save()

            else:
            	form.save()

            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!')
            return redirect('login')
    else:
        form = OrganizerRegisterForm()
    return render(request, 'users/register.html',{'form':form})

@login_required
def profile(request):
    return render(request,'users/profile.html')


@login_required
def profile_update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)   #want current pic detail instance=request.user.profile

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your Account has been Updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm()   #want current pic detail instance=request.user.profile

    context = {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request,'users/profile_update.html',context)
