import os
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from . models import User,Profile

@receiver(post_save,sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save,sender=User)
def save_profile(sender, instance,**kwargs):
    instance.profile.save()

@receiver(pre_save, sender=Profile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Profile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file =Profile.objects.get(pk=instance.pk).profile_image
    except Profile.DoesNotExist:
        return False

    new_file = instance.profile_image
    default_file = 'default.png'
    old=os.path.basename(old_file.path)
    if not old_file == new_file and not old == default_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

'''
@receiver(request_started)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Profile` object is deleted.
    """
    if instance.profile_image:
        try:
            os.path.isfile(instance.profile_image.path)
        except:
            print("Bhai teri image delete ho gyi")
            return False
'''
