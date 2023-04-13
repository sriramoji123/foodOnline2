from django.db import models
from accounts.models import User
from menu.models import FoodItem

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    fooditem= models.ForeignKey(FoodItem,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.user
    
class Tax(models.Model):
    tax_type = models.CharField(max_length=20, unique=True)
    
    #By mentioning verbose name it indicates that we want give a name by ourself
    #verbose_name is a human-readable name for the field. If the verbose name isn't given, Django will automatically create it using the field's
    tax_percentage = models.DecimalField(decimal_places=2,max_digits=4,verbose_name='Tax Percentage (%)')    

    is_active = models.BooleanField(default=True)
    
    #The verbose name will be mentioned within class Meta. Can see this in the admin page
    class Meta:
        verbose_name_plural = "Tax"
    
    def __str__(self):
        return self.tax_type