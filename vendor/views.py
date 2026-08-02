from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from accounts.forms import UserProfileForm
from menu.forms import CategoryForm, FoodItemForm
from accounts.models import UserProfile
from accounts.views import check_role_vendor
from menu.models import Category, FoodItem
from vendor.forms import VendorForm
from vendor.models import Vendor
from . import views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.defaultfilters import slugify

def get_vendor(request):
  vendor=get_object_or_404(Vendor,user=request.user)
  return vendor

# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
  profile=get_object_or_404(UserProfile,user=request.user)
  vendor=get_object_or_404(Vendor,user=request.user)
  if request.method=='POST':
    profile_form=UserProfileForm(request.POST,request.FILES,instance=profile)
    vendor_form=VendorForm(request.POST,request.FILES,instance=vendor)
    if profile_form.is_valid() and vendor_form.is_valid():
      profile_form.save()
      vendor_form.save()
      messages.success(request,'Profile Updated Successfully')
      return redirect('vprofile')
    else:
      print(profile_form.errors)
      print(vendor_form.errors)
  else:
    profile_form=UserProfileForm(instance=profile)
    vendor_form=VendorForm(instance=vendor)
  context={
    'profile_form':profile_form,
    'vendor_form':vendor_form,
    'profile':profile,
    'vendor':vendor,
  }

  return render(request,'vendor/vprofile.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
  vendor=get_vendor(request)
  categories=Category.objects.filter(vendor=vendor)
  context={
    'categories':categories,
  }

  return render(request,'vendor/menu_builder.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request,pk=None):
  vendor=get_vendor(request)
  category=get_object_or_404(Category,pk=pk)
  fooditems=FoodItem.objects.filter(vendor=vendor,category=category)
  print(fooditems)
  context={
    'fooditems':fooditems,
    'category':category,
  }

  return render(request,'vendor/fooditems_by_category.html',context) 



@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def add_category(request):
  if request.method=='POST':
    form=CategoryForm(request.POST)
    if form.is_valid():
      category_name=form.cleaned_data['Category_name']
      category=form.save(commit=False)
      category.vendor=get_vendor(request)
      category.slug=slugify(category_name)
      form.save()
      messages.success(request,'Category Added Successfully')
      return redirect('menu_builder')
    else:
      print(form.errors)
  else:
      form = CategoryForm()
  context={
  'form':form,
     }
  return render(request,'vendor/add_category.html',context)

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_category(request,pk=None):
  category=get_object_or_404(Category,pk=pk)
  if request.method=='POST':
      form=CategoryForm(request.POST,instance=category)
      if form.is_valid():
        category_name=form.cleaned_data['Category_name']
        category=form.save(commit=False)
        category.vendor=get_vendor(request)
        category.slug=slugify(category_name)
        form.save()
        messages.success(request,'Category Updated Successfully')
        return redirect('menu_builder')
      else:
        print(form.errors)
  else:
        form = CategoryForm(instance=category)
  context={
    'form':form,
    'category':category,
      }
  return render(request,'vendor/edit_category.html',context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def delete_category(request,pk=None): 
  category=get_object_or_404(Category,pk=pk)
  category.delete()
  messages.success(request,'Category Deleted Successfully')
  return redirect('menu_builder')


@login_required(login_url='login')
@user_passes_test(check_role_vendor) 
def add_food(request):
  if request.method=='POST':
    form=FoodItemForm(request.POST,request.FILES)
    if form.is_valid():
      food_title=form.cleaned_data['Food_title']
      food=form.save(commit=False)
      food.vendor=get_vendor(request)
      food.slug=slugify(food_title)
      form.save()
      messages.success(request,'Food Item Added Successfully')
      return redirect('fooditems_by_category',food.category.id)
    else:
      print(form.errors)
  else:
  
     form=FoodItemForm()
     form.fields['category'].queryset=Category.objects.filter(vendor=get_vendor(request))
  context={
    'form':form,
  }
  return render(request,'vendor/add_food.html', context)




def edit_food(request,pk=None):
  food=get_object_or_404(FoodItem,pk=pk)
  if request.method=='POST':
    form=FoodItemForm(request.POST,request.FILES,instance=food)
    if form.is_valid():
      food_title=form.cleaned_data['Food_title']
      food=form.save(commit=False)
      food.vendor=get_vendor(request)
      food.slug=slugify(food_title)
      form.save()
      messages.success(request,'Food Item Updated Successfully')
      return redirect('fooditems_by_category',food.category.id)
    else:
      print(form.errors)
  else:
  
     form=FoodItemForm(instance=food)
     form.fields['category'].queryset=Category.objects.filter(vendor=get_vendor(request))
  context={
    'form':form,
    'food':food,
  }
  return render(request,'vendor/edit_food.html', context)  



def delete_food(request,pk=None):
  food=get_object_or_404(FoodItem,pk=pk)
  food.delete()
  messages.success(request,'Food Item Deleted Successfully')
  return redirect('menu_builder')
