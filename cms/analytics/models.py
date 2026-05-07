# backend/rama_gallery/apps/analytics/models.py
from django.db import models
from django.utils import timezone
from django.db.models import Count, Sum, Q
from datetime import timedelta
import json

class AnalyticsManager(models.Manager):
    def get_dashboard_stats(self):
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        
        return {
            'total_users': self.get_total_users(),
            'new_users_today': self.get_new_users(today),
            'total_views': self.get_total_views(),
            'total_likes': self.get_total_likes(),
            'total_comments': self.get_total_comments(),
            'total_chat_messages': self.get_total_chat_messages(),
            'active_users_24h': self.get_active_users_last_24h(),
            'recent_activities': self.get_recent_activities(20),
            'content_performance': self.get_content_performance(),
            'hourly_stats': self.get_hourly_stats(today),
            'top_users': self.get_top_users(),
        }
    
    def get_total_users(self):
        from rama_gallery.apps.users.models import USERS
        return USERS.objects.count()
    
    def get_new_users(self, date):
        from rama_gallery.apps.users.models import USERS
        return USERS.objects.filter(CREATED_AT__date=date).count()
    
    def get_total_views(self):
        from rama_gallery.apps.content.models import CONTENT_ITEMS
        return CONTENT_ITEMS.objects.aggregate(total=Sum('VIEWS_COUNT'))['total'] or 0
    
    def get_total_likes(self):
        from rama_gallery.apps.content.models import LIKES
        return LIKES.objects.count()
    
    def get_total_comments(self):
        from rama_gallery.apps.content.models import COMMENTS
        return COMMENTS.objects.count()
    
    def get_total_chat_messages(self):
        from rama_gallery.apps.websocket.models import CHAT_MESSAGES
        return CHAT_MESSAGES.objects.count()
    
    def get_active_users_last_24h(self):
        from rama_gallery.apps.users.models import USER_ACTIVITY_LOGS
        last_24h = timezone.now() - timedelta(hours=24)
        return USER_ACTIVITY_LOGS.objects.filter(
            CREATED_AT__gte=last_24h
        ).values('USER_ID').distinct().count()
    
    def get_recent_activities(self, limit=20):
        from rama_gallery.apps.users.models import USER_ACTIVITY_LOGS
        return USER_ACTIVITY_LOGS.objects.select_related('USER_ID').order_by('-CREATED_AT')[:limit]
    
    def get_content_performance(self):
        from rama_gallery.apps.content.models import CONTENT_ITEMS
        return list(CONTENT_ITEMS.objects.filter(IS_PUBLISHED=True).order_by('-VIEWS_COUNT')[:10].values(
            'ID', 'TITLE', 'VIEWS_COUNT', 'LIKES_COUNT', 'COMMENTS_COUNT'
        ))
    
    def get_hourly_stats(self, date):
        from rama_gallery.apps.content.models import VIEWS_TRACKING
        hourly_data = []
        for hour in range(24):
            start_time = timezone.make_aware(timezone.datetime.combine(date, timezone.datetime.min.time().replace(hour=hour)))
            end_time = start_time + timedelta(hours=1)
            count = VIEWS_TRACKING.objects.filter(CREATED_AT__range=(start_time, end_time)).count()
            hourly_data.append({'hour': hour, 'count': count})
        return hourly_data
    
    def get_top_users(self):
        from rama_gallery.apps.users.models import USERS
        from django.db.models import Count
        return list(USERS.objects.annotate(
            content_count=Count('CONTENT_ITEMS'),
            likes_received=Count('CONTENT_ITEMS__LIKES'),
            comments_made=Count('COMMENTS')
        ).order_by('-likes_received')[:10].values('USERNAME', 'content_count', 'likes_received', 'comments_made'))

analytics_manager = AnalyticsManager()