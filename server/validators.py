from PIL import Image
from django.core.exceptions import ValidationError
import os
def validate_icon_image(image):
    if image:
        with Image.open(image) as img:
            if img.width>70 or img.height>70:
                raise ValidationError(detail=f"The maximum dimensions for allowed image are 70x70. Size recived: {img.size}")

def validate_image_ext(image):
    ext=os.path.split(image.name)[1]

    valid_ext=['.png','.jpeg','.gif']
    if ext.lower() not in valid_ext:
        raise ValidationError(detail=f"Only .png, .jpeg and .gif files are allowed. File recived: {ext}")