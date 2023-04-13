from django.shortcuts import get_object_or_404, render
from vendor.models import Vendor, OpeningHour
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from .models import Cart
from .context_processors import get_cart_counter, get_cart_amounts
from django.contrib.auth.decorators import login_required  
from django.db.models import Q

from datetime import date,datetime

def marketplace(request):
    vendors= Vendor.objects.filter(is_approved= True, user__is_active=True)
    vendor_count = vendors.count()
    context={
        'vendors' : vendors,
        'vendor_count' : vendor_count
    }     
    
    return render(request,'marketplace/listings.html',context)

def vendor_detail(request,vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True )
        )
    )
    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day','-from_hour')
    
    
    today_date = date.today()
    today = today_date.isoweekday()
    
    current_opening_hour = OpeningHour.objects.filter(vendor=vendor,day=today)
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor' : vendor,
        'categories' : categories,
        'cart_items':cart_items,
        'opening_hours':opening_hours, 
        'current_opening_hour' : current_opening_hour ,
         
    }
    return render(request,'marketplace/vendor_detail.html',context)

def add_to_cart(request,food_id):
    if request.user.is_authenticated:
        #this is to check if we are getting any ajax request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                #check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user,fooditem=fooditem)
                    chkCart.quantity+=1
                    chkCart.save()
                   
                    return JsonResponse({"status":'Success','message':"Increased the cart quantity",'cart_counter':get_cart_counter(request),'qty':chkCart.quantity, 'cart_amount':get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user,fooditem=fooditem,quantity=1)
                    return JsonResponse({"status":'Success','message':"Added the food to Cart",'cart_counter':get_cart_counter(request),'qty':chkCart.quantity, 'cart_amount':get_cart_amounts(request)})
            except:
                return JsonResponse({"status":'Failed','message':"This food id does not exist"})                
        else:
            return JsonResponse({"status":'Failed','message':"Invalid request!"})            
    else:
        return JsonResponse({"status":'login_required','message':"Please login to continue"})


def decrease_cart(request,food_id):
    if request.user.is_authenticated:
        #this is to check if we are getting any ajax request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #Check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                #check if the user has already added that food to the cart
                try:
                    chkCart = Cart.objects.get(user=request.user,fooditem=fooditem)
                    if chkCart.quantity > 1:    
                        chkCart.quantity-=1
                        chkCart.save()
                    else:
                        chkCart.quantity=0
                        chkCart.delete()

#here get_cart_counter and get_cart_amounts both are functions present in context processor
                    return JsonResponse({"status":'Success','message':"Decreased the cart quantity",'cart_counter':get_cart_counter(request),'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})
                except:
                    return JsonResponse({"status":'Failed','message':"You do not have this food in your Cart"})
            except:
                return JsonResponse({"status":'Failed','message':"This food id does not exist"})                
        else:
            return JsonResponse({"status":'Failed','message':"Invalid request!"})            
    else:
        return JsonResponse({"status":'login_required','message':"Please login to continue"})


@login_required(login_url = 'login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    
    context = {
        'cart_items':cart_items,
    }
    return render(request,'marketplace/cart.html',context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({"status":'Success','message':"Cart item has been deleted","cart_counter":get_cart_counter(request),'cart_amount':get_cart_amounts(request)})    
            except:
                return JsonResponse({"status":'Failed','message':"Cart item does not exist"})
                
        else:   
            return JsonResponse({"status":'Failed','message':"Invalid request!"})  
        
    
def search(request):
    keyword = request.GET["keyword"]
    
    fetch_vendors_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword, is_available= True).values_list('vendor',flat=True)
    print(fetch_vendors_by_fooditems)
    
    vendors=Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True,user__is_active=True))
    vendors_count = vendors.count()
    context={
        'vendors':vendors,
        'vendors_count':vendors_count
        }
    
    return render(request,"marketplace/listings.html",context)
    
    
    