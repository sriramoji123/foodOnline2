from .models import Cart, Tax
from menu.models import FoodItem


def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count+=cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count=cart_count)


def get_cart_amounts(request):
    print("called")
    subtotal = 0
    tax= 0
    grand_total = 0
    if request.user.is_authenticated:
        cart_items=Cart.objects.filter(user=request.user)
        for item in cart_items:
            fooditem = FoodItem.objects.get(pk=item.fooditem.id)
            subtotal += (fooditem.price * item.quantity)
        
        tax_dict={}
        
        get_tax = Tax.objects.filter(is_active=True)
        for i in get_tax:
            tax_type= i.tax_type
            tax_percentage = i.tax_percentage
            tax_amount = round((tax_percentage * subtotal)/100,2)
            print(tax_type,tax_percentage,tax_amount)
            
            #{'CGST': {Decimal('9.00'): Decimal('3.78')}, 'IGST': {Decimal('5.00'): Decimal('2.10')}}
            tax_dict.update({tax_type:{str(tax_percentage):tax_amount}})
            
        tax=0    
        for key in tax_dict.values():
            for x in key.values():
                tax+=x
        
        #can also be calculated as follows
        # tax = sum(x for key in tax_dict.values() for x in key.values())
        grand_total = subtotal + tax
        print(grand_total)
        print(tax_dict)
    return dict(subtotal=subtotal, tax=tax, grand_total=grand_total,tax_dict=tax_dict)    
    