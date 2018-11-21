from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from catalogue.models import Snippet, Category
from django.core.exceptions import ObjectDoesNotExist

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	token = models.TextField(max_length=500, blank=True)

	snippets = models.ManyToManyField(Snippet)
	categories = models.ManyToManyField(Category)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	try : 
	    instance.userprofile.save()
	except ObjectDoesNotExist : 
		pass 