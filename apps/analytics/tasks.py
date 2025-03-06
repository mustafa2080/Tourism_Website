# analytics/tasks.py
from celery import shared_task
from apps.analytics.models import Visitor

@shared_task
def update_visitor_analytics():
    visitors = Visitor.objects.all()
    for visitor in visitors:
        visitor.increment_visit_count()