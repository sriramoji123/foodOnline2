from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile



#this is like sender and receiver jobs 
#here any action happens on User db then post saving it the below methos will execute
#the parameters names should be as it is
#created indicates if the action is done successfully or not.
#if the save is successful then created will be true
#post impleting this function Create a user from admin page then the below function will be executed

@receiver(post_save,sender=User)
#sender is the model
#instance is either created or altered
#created is either true or false
def post_save_create_profile_receiver(sender,instance,created,**kwargs):
    print(created)
    if created:
        
    #write the logic to create the user profile automatically
        UserProfile.objects.create(user=instance)
    

    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
        except:
            UserProfile.objects.create(user=instance)
     
