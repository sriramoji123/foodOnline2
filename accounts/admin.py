from django.contrib import admin
from .models import User,UserProfile
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','username','role','is_active')
    ordering = ['-date_joined']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

# Register your models here.
#this is to make sure that you can see the users list in admin page 
admin.site.register(User,CustomUserAdmin)
admin.site.register(UserProfile)
