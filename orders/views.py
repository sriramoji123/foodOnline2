from django.http import HttpResponse
from random import randint
import simplejson as json
from django.shortcuts import redirect, render
from accounts.utils import send_notification
from marketplace.context_processors import get_cart_amounts
from django.contrib.auth.decorators import login_required

from marketplace.models import Cart
from orders.forms import OrderForm
from orders.models import Order, OrderedFood, Payment
from .utils import generate_order_number

# Create your views here.
@login_required(login_url='login')
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('marketplace')
    subtotal = get_cart_amounts(request)['subtotal']
    total_tax = get_cart_amounts(request)['tax']
    grand_total = get_cart_amounts(request)['grand_total']
    tax_data = get_cart_amounts(request)['tax_dict']
    
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city'] 
            order.pin_code = form.cleaned_data['pin_code'] 
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            order.save()
            order.order_number = generate_order_number(order.id)
            request.session['order_no'] = order.order_number
            order.save()
            context = {
                'order':order,
                'cart_items':cart_items,
            }
            return render(request, 'orders/placeorder.html',context)
        else:
            print(form.errors)
    return render(request, 'orders/placeorder.html')



@login_required(login_url='login')
def payments(request):
    #Store the payment details in the payment model
    order_number = request.session['order_no']
    transaction_id = randint(100000, 9999999)
    payment_method = "COD"
    status = "Accepted"
    print(order_number, transaction_id, payment_method, status)
    
    
    order = Order.objects.get(user=request.user,order_number=order_number)
    payment = Payment(
        user= request.user,
        transaction_id = transaction_id,
        payment_method = payment_method,
        amount= order.total,
        status = status
        
    )
    payment.save()
    #Payment model will get saved by this point. You can verify
    
    
    #UPDATE THE ORDER MODEL
    order.payment = payment
    order.is_ordered = True 
    order.save()
  


    #Move the cart items to ordered food model
    cartitems = Cart.objects.filter(user=request.user)
    for item in cartitems:
        ordered_food = OrderedFood()
        ordered_food.order = order
        ordered_food.payment = payment
        ordered_food.user = request.user
        ordered_food.fooditem = item.fooditem
        ordered_food.quantity = item.quantity
        ordered_food.price = item.fooditem.price
        ordered_food.amount = item.fooditem.price * item.quantity
        ordered_food.save()
        
    

        
    #Send order confirmation email to user
    mail_subject = "Thank you for ordering with us"
    mail_template = 'orders/order_confirmation_email.html'
    context ={
        'user':request.user,
        'order':order,
        'to_email':order.email,
    }
    send_notification(mail_subject,mail_template,context)

    #Send order confirmation emails to vendors
    mail_subject = "You have received an order"
    mail_template = 'orders/new_order_received.html'
    to_emails=[]
    for i in cartitems:
        if i.fooditem.vendor.user.email not in to_emails:
            to_emails.append(i.fooditem.vendor.user.email)
    context ={
        'user':request.user,
        'to_email':to_emails,
    }
    print("the emails are")
    print(to_emails)
    send_notification(mail_subject,mail_template,context)
    
    
    #CLEAR THE CART
    cartitems.delete()

    return HttpResponse('Success')