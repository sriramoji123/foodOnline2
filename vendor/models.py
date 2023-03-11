from django.db import models
from accounts.models import User,UserProfile
from accounts.utils import send_notification
# Create your models here.
class Vendor(models.Model):
    user=models.OneToOneField(User,related_name='user',on_delete=models.CASCADE)
    user_profile=models.OneToOneField(UserProfile,related_name='userprofile',on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.vendor_name
    
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
                        'is_approved': self.is_approved
                    }
                if self.is_approved == True:
                    mail_subject='Congratulations! your account has been approved'
                    send_notification(mail_subject,mail_template,context)
                else:
                    mail_subject="We're Sorry ! you are not eligible for publishing your food menu on our template"
                    send_notification(mail_subject,mail_template,context)
        return super(Vendor,self).save(*args,**kwargs)
    
                    