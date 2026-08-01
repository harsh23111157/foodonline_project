from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User,UserProfile
from django.contrib import messages,auth
from vendor.forms import VendorForm
from django.contrib.auth import authenticate,login
from .utils import detectUser,send_verification_email
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendor.models import Vendor

# Create your views here.
# restrict the vendor accesing the custome page
def check_role_vendor(user):
  if user.role == 1:
    return True
  else:
    raise PermissionDenied

 


# restrict the customer accesing the vendor page
def check_role_customer(user):
  if user.role == 2:
    return True
  else:
    raise PermissionDenied


  




def registerUser(request):
  if request.user.is_authenticated:
      messages.warning(request,'you are already logged in')
      return redirect('dashboard')
  elif request.method == 'POST':
    print(request.POST)
    form=UserForm(request.POST)
    if form.is_valid():
      # password=form.cleaned_data['password']
      # user=form.save(commit=False)
      # user.set_password(password)
      # user.role=User.CUSTOMER
      # user.save()
      # return redirect('registerUser')

      first_name=form.cleaned_data['first_name']
      last_name=form.cleaned_data['last_name']
      username=form.cleaned_data['username']
      email=form.cleaned_data['email']
      password=form.cleaned_data['password']
      user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
      user.role=User.CUSTOMER
      user.save()
      #send verification email


      #send verification email
      mail_subject='please activate your account'
      email_template='accounts/email/account_verification_email.html'
      send_verification_email(request,user,mail_subject,email_template)
       

      messages.success(
            request, 
            f"Registration successful! An activation link has been sent to {email}. "
            f"Please check your email inbox and verify your account before logging in."
        )
      print('user is created')
      return redirect('registerUser')
    else:
      print(form.errors)
    


  else:
    form=UserForm()
  context={
    'form':form,
  }
  return render(request,'accounts/registerUser.html',context)
  



def registerVendor(request):
  if request.user.is_authenticated:
      messages.warning(request,'you are already logged in')
      return redirect('myAccount')
  elif request.method == 'POST':
    form=UserForm(request.POST)
    v_form=VendorForm(request.POST,request.FILES)
    if form.is_valid() and v_form.is_valid():
      first_name=form.cleaned_data['first_name']
      last_name=form.cleaned_data['last_name']
      username=form.cleaned_data['username']
      email=form.cleaned_data['email']
      password=form.cleaned_data['password']
      user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
      user.role=User.VENDOR
      user.save()
      vendor=v_form.save(commit=False)
      vendor.user=user
      user_profile=UserProfile.objects.get(user=user)
      vendor.user_profile=user_profile
      vendor.save()
      #send verification email
      mail_subject='please activate your account'
      emai_template='accounts/email/account_verification_email.html'
      send_verification_email(request,user,mail_subject,emai_template)


      messages.success(
            request, 
            f"Your account has been created successfully! We have sent a verification link to {email}. "
            f"Please check your email to activate your account. Note: Final access is subject to admin approval."
        )
      return redirect('registerVendor')
      
    else:
      print('invalid form')
      print(form.errors)

    
  else:
      form=UserForm()
      v_form=VendorForm()
  context={
    'form':form,
    'v_form':v_form,
  }

  return render(request,'accounts/registerVendor.html',context)



def activate(request,uid64,token):
  #by this activate the user settings as is_active status to true
  try:
    uid=urlsafe_base64_decode(uid64).decode()
    user=User.objects.get(pk=uid)
  except(TypeError,ValueError,OverflowError,User.DoesNotExist):
    user=None

  if user is not None and default_token_generator.check_token(user,token):
    user.is_active=True
    user.save()
    messages.success(request,'Account verified successfully')
    return redirect('myAccount')
  else:
    return redirect('myAccount')

  return


def login(request):
  if request.user.is_authenticated:
    messages.warning(request,'you are already logged in')
    return redirect('myAccount')
  elif request.method == 'POST':
    email=request.POST['email']
    password=request.POST['password']

    user=auth.authenticate(email=email,password=password)
    if user is not None:
      auth.login(request,user)
      messages.success(request,"you arre now logged in")
      return redirect('myAccount')
    else:
      messages.error(request,"there is an error,invalid login credential")
      return redirect('login')
    
  return render(request,'accounts/login.html')

def logout(request):
  auth.logout(request)
  messages.info(request,"you are now logged out ")
  return redirect('login')
  
@login_required(login_url='login')
def myAccount(request):
  user=request.user
  redirecturl = detectUser(user)
  return redirect(redirecturl)
  

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
  return render(request,'accounts/custDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
  
  return render(request,'accounts/vendorDashboard.html')


def forgot_password(request):
  if request.method == 'POST':
    email=request.POST['email']


    if User.objects.filter(email=email).exists():
      user=User.objects.get(email__exact=email)

      #send reste password email
      mail_subject='reset your password'
      emai_template='accounts/email/reset_password_email.html'
      send_verification_email(request,user,mail_subject,emai_template)

      messages.success(request,'password reset link has been sent to your email adress')
      return redirect('login')
    else:
      messages.error(request,'account does not exist')
      return redirect('forgot_password')
  return render(request,'accounts/forgot_password.html')


def reset_password_validate(request,uid64,token):
  try:
      uid=urlsafe_base64_decode(uid64).decode()
      user=User.objects.get(pk=uid)
  except(TypeError,ValueError,OverflowError,User.DoesNotExist):
      user=None

  if user is not None and default_token_generator.check_token(user,token):
    request.session['uid']=uid
    messages.info(request,'please reset your password')
    return redirect('reset_password')
  else:
    messages.error(request,'this link has been expired')
    return redirect('myAccount')

   


def reset_password(request):
  if request.method == 'POST':
    password=request.POST['password']
    confirm_password=request.POST['confirm_password']

    if password == confirm_password:
      pk=request.session.get('uid')
      user=User.objects.get(pk=pk)
      user.set_password(password)
      user.is_active=True
      user.save()
      messages.success(request,'password reset sucessful')
      return redirect('login')
    else:
      messages.error(request,'password dont match')
      return redirect('reset_password')
  return render(request,'accounts/reset_password.html')  


      
  




