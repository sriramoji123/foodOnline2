from django.db import models
from accounts.models import User,UserProfile
from accounts.utils import send_notification
from datetime import time, date, datetime
# Create your models here.


class Vendor(models.Model):
    user=models.OneToOneField(User,related_name='user',on_delete=models.CASCADE)
    user_profile=models.OneToOneField(UserProfile,related_name='userprofile',on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug= models.SlugField(max_length=100,unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.vendor_name
    
    #All the member functions must have self as a parameter by default
    def is_open(self):
        today_date = date.today()
        today = today_date.isoweekday()
        
        #Since self returns vendor_name which is the required thing we are just passing in the below line
        current_opening_hour = OpeningHour.objects.filter(vendor=self,day=today)
        now= datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(type(current_time))
        
        is_open = None
        for i in current_opening_hour:
            #This condition is written to check if the day is closed or not
            #Because if the day is closed there start and end times will not be 
            #submitted. and hence while retrieving them it throws an error.
            if not i.is_closed:
                start = str(datetime.strptime(i.from_hour,"%I:%M %p").time())
                end = str(datetime.strptime(i.to_hour,"%I:%M %p").time())
            
                if current_time > start and current_time < end:
                    is_open = True
                    break
                else:
                    is_open = False
        return is_open
    
    def save(self,*args,**kwargs):
        #This condition is to check if we are creating a new vendor or changing the existing one.
        #Since we want to send a separate email only in case of altering we write this
        if self.pk is not None:
            #Updating the existing
            orig = Vendor.objects.get(pk=self.pk)
            
            #This is to check if there is any change after saving the form
            if orig.is_approved != self.is_approved:
                mail_template='accounts/emails/admin_approval_email.html'
                context={
                        'user': self.user,
                        'is_approved': self.is_approved,
                        'to_email': self.user.email
                    }
                if self.is_approved == True:
                    mail_subject='Congratulations! your account has been approved'
                    send_notification(mail_subject,mail_template,context)
                else:
                    mail_subject="We're Sorry ! you are not eligible for publishing your food menu on our template"
                    send_notification(mail_subject,mail_template,context)
        return super(Vendor,self).save(*args,**kwargs)
    


DAYS=[
     (1,("Monday")),
     (2,("Tuesday")),
     (3,("Wednesday")),
     (4,("Thursday")),
     (5,("Friday")),
     (6,("Saturday")),
     (7,("Sunday")),
     
]

HOUR_OF_DAY_24=[(time(h,m).strftime('%I:%M %p'),time(h,m).strftime('%I:%M %p'))  for h in range(0,24) for m in (0,30)]
class OpeningHour(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24,max_length=20,blank=True)    
    to_hour = models.CharField(choices=HOUR_OF_DAY_24,max_length=20,blank=True)
    is_closed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('day','-from_hour')
        
        # Sets of field names that, taken together, must be unique
        #The reason for adding this is lets say we have added opening time on Monday 10 2 & Monday 10 2. It throws an error
        unique_together = ('vendor','day','from_hour','to_hour')
        
    def __str__(self):
        return self.get_day_display()