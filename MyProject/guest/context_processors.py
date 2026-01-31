from .models import Notification


def notifications(request):
    if request.user.is_authenticated:
        unread_qs = Notification.objects.filter(user=request.user, is_read=False).order_by('-timestamp')
        recent_qs = Notification.objects.filter(user=request.user).order_by('-timestamp')[:5]
        return {
            'unread_notifications': unread_qs,
            'unread_notifications_count': unread_qs.count(),
            'recent_notifications': recent_qs,
        }
    return {
        'unread_notifications': [],
        'unread_notifications_count': 0,
        'recent_notifications': [],
    }
