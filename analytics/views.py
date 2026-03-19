from django.shortcuts import render
from django.db.models import Count, Sum
from .models import Visitor, VisitLog
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

@user_passes_test(lambda u: u.is_superuser) 
def analytics_dashboard(request):
    total_visitors = Visitor.objects.count()
    total_visits = VisitLog.objects.count()
    
    today = timezone.now().date()
    visitors_today = Visitor.objects.filter(created_at__date=today).count()

    browser_stats = Visitor.objects.values('browser').annotate(
        count=Count('browser')
    ).order_by('-count')[:5]

    os_stats = Visitor.objects.values('os').annotate(
        count=Count('os')
    ).order_by('-count')

    top_pages = VisitLog.objects.values('page_url').annotate(
        view_count=Count('page_url')
    ).order_by('-view_count')[:10]

    recent_logs = VisitLog.objects.select_related('visitor').order_by('-entry_time')[:10]

    context = {
        'total_visitors': total_visitors,
        'total_visits': total_visits,
        'visitors_today': visitors_today,
        'browser_stats': browser_stats,
        'os_stats': os_stats,
        'top_pages': top_pages,
        'recent_logs': recent_logs,
    }

    return render(request, 'analytics/dashboard.html', context)