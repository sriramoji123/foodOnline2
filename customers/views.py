from django.shortcuts import render, get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm, UserInfoForm
from accounts.models import UserProfile
from django.contrib import messages
# Create your views here.
def cprofile(request):
    profile = get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        print("called to post method")
        profile_form = UserProfileForm(request.POST,request.FILES,instance=profile)
        user_form = UserInfoForm(request.POST,request.FILES,instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request,'Profile updated')
            return redirect('cprofile') 
        else:
            print(profile_form.errors)
            print(user_form.errors)
    else:
        print("called to get method")
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=request.user)   
    context={
        'profile_form' : profile_form,
        'user_form' : user_form,
        'profile' : profile,
    }
    
    return render(request, 'customers/cprofile.html',context)
