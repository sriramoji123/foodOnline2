from django.shortcuts import get_object_or_404, render
from vendor.models import Vendor
from menu.models import Category, FoodItem
from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from .models import Cart
from .context_processors import get_cart_counter
from django.contrib.auth.decorators import login_required  

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
    
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor' : vendor,
        'categories' : categories,
        'cart_items':cart_items,    
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
                    return JsonResponse({"status":'Success','message':"Increased the cart quantity",'cart_counter':get_cart_counter(request),'qty':chkCart.quantity})
                except:
                    chkCart = Cart.objects.create(user=request.user,fooditem=fooditem,quantity=1)
                    return JsonResponse({"status":'Success','message':"Added the food to Cart",'cart_counter':get_cart_counter(request),'qty':chkCart.quantity})
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
                    if chkCart.quantity >= 1:    
                        chkCart.quantity-=1
                        chkCart.save()
                    else:
                        chkCart.quantity=0
                        chkCart.delelete()

                    return JsonResponse({"status":'Success','message':"Decreased the cart quantity",'cart_counter':get_cart_counter(request),'qty':chkCart.quantity})
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
    cart_items = Cart.objects.filter(user= request.user).order_by('created_at')
    
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
                    return JsonResponse({"status":'Success','message':"Cart item has been deleted","cart_counter":get_cart_counter(request)})    
            except:
                return JsonResponse({"status":'Failed','message':"Cart item does not exist"})
                
        else:   
            return JsonResponse({"status":'Failed','message':"Invalid request!"})  
        
    