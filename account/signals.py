from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import Customer, CustomerProfile


@receiver(post_save, sender=Customer)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        CustomerProfile.objects.create(
            customer=instance
        )



