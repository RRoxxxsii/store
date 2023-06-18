from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import Product


@receiver(post_save, sender=Product)
def update_category_is_active(sender, instance, created, **kwargs):
    if created and instance.is_active:
        instance.category.is_active = True
        instance.category.save()
