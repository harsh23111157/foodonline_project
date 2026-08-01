from django.core.exceptions import ValidationError
import os

def allow_only_images_validator(value):
  valid_extensions=['jpg','jpeg','png']
  ext=os.path.splitext(value.name)[1]
  if not ext.lower() in valid_extensions:
    raise ValidationError('Unsupported file extension. Allowed extensions are: {}'.format(', '.join(valid_extensions)))