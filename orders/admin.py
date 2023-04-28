from django.contrib import admin

from .models import Payment, Order, OrderedFood
# Register your models here.

class OrderedFoodOnline(admin.TabularInline):
    model = OrderedFood
    #To make sure that these fields are not editable from user side
    readonly_fields = ('order','payment','fooditem','quantity','price','amount')
    #This is to display on the rows which are present in the orderedfood page. If not written will utilize the complete space of the ui screen.
    extra = 0
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','name','phone','email','total','payment_method','status','is_ordered']
    inlines = [OrderedFoodOnline]
    
    
admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderedFood)