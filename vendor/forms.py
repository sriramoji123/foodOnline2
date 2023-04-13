from django import forms
from .models import Vendor, OpeningHour
from accounts.validators import allow_only_images_validator

class VendorForm(forms.ModelForm):
    #This is to change the default upload option. Check the onenote. to find the difference.
    #Normal file upload is added with some padding and blue clor
    vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images_validator])
    class Meta:
        model = Vendor
        fields=['vendor_name','vendor_license']
        
class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields=['day','from_hour','to_hour','is_closed']
        
        
        