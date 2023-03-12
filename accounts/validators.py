from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
    print(value)
    ext = os.path.splitext(value.name)[1] #cover_image.jpg --> jpg
    print(ext)
    
    valid_extensions=['.png','.jpg','.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extensions. Allowed extensions: '+str(valid_extensions))
    