import uuid
from .models import Visitor, VisitLog

class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

        if ip in ['127.0.0.1', '::1']:
            return self.get_response(request)

      
        if hasattr(request, 'user') and request.user.is_authenticated and request.user.is_staff:
            return self.get_response(request)

        user_agent_str = request.META.get('HTTP_USER_AGENT', '')
        
        browser = "Other"
        if "Chrome" in user_agent_str: browser = "Chrome"
        elif "Safari" in user_agent_str: browser = "Safari"
        
        os = "Other"
        if "Windows" in user_agent_str: os = "Windows"
        elif "Macintosh" in user_agent_str: os = "MacOS"
        elif "iPhone" in user_agent_str: os = "iOS"

        device_id = request.COOKIES.get('device_id')
        
        visitor, created = Visitor.objects.get_or_create(
            device_id=device_id or str(uuid.uuid4()),
            defaults={'ip_address': ip, 'browser': browser, 'os': os}
        )

        if not any(request.path.startswith(p) for p in ['/admin/', '/static/', '/media/', '/analytics/']):
            VisitLog.objects.create(
                visitor=visitor,
                page_url=request.path,
                referrer=request.META.get('HTTP_REFERER', '')
            )

        response = self.get_response(request)
        
        if not device_id:
            response.set_cookie('device_id', str(visitor.device_id), max_age=31536000)

        return response