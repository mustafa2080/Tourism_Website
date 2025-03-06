# analytics/middleware.py
from apps.analytics.models import Visitor

class VisitorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')
        referrer = request.META.get('HTTP_REFERER', '')

        # البحث عن الزوار بنفس العنوان IP
        visitors = Visitor.objects.filter(ip_address=ip_address)

        if visitors.exists():
            # إذا وجدت زوارًا بنفس العنوان IP، اختر أول واحد
            visitor = visitors.first()
            visitor.increment_visit_count()
        else:
            # إذا لم يوجد، قم بإنشاء زائر جديد
            visitor = Visitor.objects.create(
                ip_address=ip_address,
                user_agent=user_agent,
                referrer=referrer,
                user=request.user if request.user.is_authenticated else None,
            )

        response = self.get_response(request)
        return response