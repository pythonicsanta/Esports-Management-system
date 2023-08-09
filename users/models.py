from django.db import models
#from blog.models import Post
from django.contrib.auth.models import AbstractUser
from PIL import Image

# Create your models here.
class User(AbstractUser):
    is_organizer = models.BooleanField(default=False)

    def __str__(self):
        return(self.username )

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(default='default.png',upload_to='profile_pics',blank=True)
    


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):       # this fn resizes image size

        super(Profile,self).save(*args, **kwargs)
        img = Image.open(self.profile_image.path)

        if img.height >300 or img.width >300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)
