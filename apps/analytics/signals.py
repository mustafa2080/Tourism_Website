# analytics/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.analytics.models import Visitor

@receiver(post_save, sender=Visitor)
def update_visitor_count(sender, instance, **kwargs):
    print(f"Visitor {instance.ip_address} was saved!")