from internships.models import Notification
from user_management.models import Student


def unread_notifications_processor(request):
    """
    Context processor to inject unread notification count
    for authenticated student users across all templates.
    """
    if request.user.is_authenticated:
        try:
            student = Student.objects.filter(user=request.user).first()
            if student:
                count = Notification.objects.filter(student=student, is_read=False).count()
                return {'unread_notifications_count': count}
        except Exception:
            pass
    return {'unread_notifications_count': 0}
