from django import forms
from .models import User
class UserForm(forms.ModelForm):
    password= forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields=["first_name","last_name","username","email","phone_number","password"]
    
    
    #this is used to display any non field errors. check in registerUser.html page 
    # <li style="color: red">
    #                   {{form.non_field_errors}}
    #                 </li>
    def clean(self):
        cleaned_data = super(UserForm,self).clean()
        password=cleaned_data.get("password")
        confirm_password=cleaned_data.get("confirm_password")
        
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        if password == "a":
            raise forms.ValidationError("password should not be a")