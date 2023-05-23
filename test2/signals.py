from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth.models import Group


def customer_profile(sender, instance, created, **kwargs):

    """
        Signal handler to create a customer profile for a newly created user.

        Parameters:
            sender (class): The class that sent the signal (User model).
            instance (object): The actual instance being saved (User instance).
            created (bool): Indicates if the instance was just created.
            kwargs (dict): Additional keyword arguments passed to the signal.

        Returns:
            None
        """
    
    if created and not instance.is_staff:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        
        Customer.objects.create(
            user=instance,
            name=instance.username
        )

# DisConnect the customer_profile signal handler to the post_save signal of the User model
post_save.disconnect(customer_profile, sender=User)
