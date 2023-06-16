from datetime import timedelta, datetime
from django.conf import settings
from django.utils import timezone
import stripe
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class BaseModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Plan(BaseModel):
    RECURRING_FREQ_CHOICES = (
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ('once', 'Once')
    )

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='plans', null=True)
    plan_name = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    article_read_limit = models.IntegerField()
    price_id = models.CharField(max_length=50, blank=True, null=True)
    recurring_freq = models.CharField(max_length=50, choices=RECURRING_FREQ_CHOICES)
    is_recurring = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.plan_name} - {self.recurring_freq} wise"

@receiver(post_save, sender=Plan)
def create_stripe_product_and_price(sender, instance, created, **kwargs):
    if created:
        # Create a product in Stripe
        product = stripe.Product.create(
            name=instance.plan_name,
            type='service',
        )

        # Create a price in Stripe based on the plan's details
        if instance.is_recurring:
            if instance.recurring_freq == 'monthly':
                interval = 'month'
            elif instance.recurring_freq == 'yearly':
                interval = 'year'
            else:
                interval = None

            if interval:
                price = stripe.Price.create(
                    unit_amount=int(instance.price) * 100,
                    currency='inr',
                    recurring={'interval': interval},
                    product=product.id,
                )
                instance.price_id = price.id  # Store the price object ID in the price_id field
        else:
            price = stripe.Price.create(
                unit_amount=int(instance.price) * 100,
                currency='inr',
                product=product.id,
            )
            instance.price_id = price.id  # Store the price object ID in the price_id field

        instance.save()  # Save the updated instance


class Subscription(BaseModel):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)
    customer_id = models.CharField(max_length=50, null=True)
    payment_id = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, null=True)
    expire_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "Subscription"

    def has_expired(self):
        now = timezone.now()
        if self.expire_at:
            expire_date = self.expire_at.date()
            expire_time = self.expire_at.time()
            return now.date() > expire_date or (now.date() == expire_date and now.time() > expire_time)
        return False

class Restrict(models.Model):
    post = models.IntegerField()
    read_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - Post ID: {self.post}"   