
from django.conf import settings

from books.models import Order
from .forms import PasswordChangeFormUser, UserCreationForm,LoginForm,VerifyForm
from django.http.response import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .models import PreRegistration
from django.contrib.auth.models  import auth,User
from django.shortcuts import render
import random
from django.contrib import messages
from django.shortcuts import render,redirect
from django.core.mail import send_mail



#Create your views here.

def creatingOTP():
    otp = ""
    for i in range(5):
        otp+= f'{random.randint(0,9)}'
    return otp

def sendEmail(email,first_name,last_name):
    otp = creatingOTP()
    email_message = f"""
Dear {first_name} {last_name},
******* This is an automated email. Please do not reply to this email.******* 

Your One Time Password (OTP ) is {otp}.

If you have any queries, Please contact us at,
BookWorld@Gmail.Com,
Contact 977-01-1234565

Thanks & regards
BookWorld Limited
Gokarneshwor,Kathmandu, Nepal"""

    send_mail(
    'One Time Password',
    email_message,
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
    )
    return otp




def SignUp_function(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            email = request.POST.get('email')
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            username=request.POST.get('username')

            if form.is_valid():
                if User.objects.filter(email=email).exists():
                    messages.info(request,'Email already taken')
                    return redirect('/reg')
                if User.objects.filter(username=username).exists():
                    messages.info(request,'Username already taken')
                    return redirect('/reg')
                else:
                     email=form.cleaned_data['email']
                     otp = sendEmail(email,first_name,last_name)
                     dt = PreRegistration(first_name=form.cleaned_data['first_name'],last_name=form.cleaned_data['last_name'],username= form.cleaned_data['username'],email=email,otp=otp,password1 = form.cleaned_data['password1'],password2 = form.cleaned_data['password2'])
                     dt.save()
                    #  messages.success(request, 'Account is created Successfully!')
                     return HttpResponseRedirect('/verify/')

        else:
            form = UserCreationForm()
        return render(request,'register.html',{'form':form})
    else:
        return HttpResponseRedirect('/')




def Login_function(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')
            # Authenticate the user using Django's built-in authentication system
            user = authenticate(request, username=username, password=password)
            # If the user credentials are valid, log them in and redirect to homepage
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'login.html', context)


    
   

def verifyUser(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = VerifyForm(request.POST)
            if form.is_valid():
                otp = form.cleaned_data['otp']
                data = PreRegistration.objects.filter(otp = otp)
                # If the OTP exists, retrieve the user details from the PreRegistration table
                if data:
                    username = ''
                    first_name = ''
                    last_name = ''
                    email = ''
                    password1 = ''
                    for i in data:
                        print(i.username)
                        username = i.username
                        first_name = i.first_name
                        last_name = i.last_name
                        email = i.email
                        password1 = i.password1
               
                    # Create a new user with the retrieved details
                    user = User.objects.create_user(username, email, password1)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    data.delete()
                    messages.success(request,'Account is created successfully!')
                    return HttpResponseRedirect('/login')   
                else:
                    messages.success(request,'Entered OTP is wrong')
                    return HttpResponseRedirect('/verify/')
        else:            
            form = VerifyForm()
        return render(request,'verify.html',{'form':form})
    else:
        return HttpResponseRedirect('/login')






def changePassword(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user.username,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        if request.method == 'POST':
            changePasswordForm = PasswordChangeFormUser(user=request.user,data= request.POST)
            if changePasswordForm.is_valid():
                changePasswordForm.save()
                messages.success(request,"Your password is changed successfully !!")
                return HttpResponseRedirect('/login')
                
        else:
            changePasswordForm = PasswordChangeFormUser(user=request.user)
        return render(request,'chngepassword.html',{'passwordForm':changePasswordForm,'order':order,'items':items,'cartItems':cartItems})
    else:
        return HttpResponseRedirect('/store')